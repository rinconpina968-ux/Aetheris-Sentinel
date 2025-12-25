/**
 * PROYECTO: AETHERIS SENTINEL v3.5
 * MÓDULO: Kernel Sensor & Network Auditor
 * ESTÁNDAR: C++17 / Win32 API
 * * DESCRIPCIÓN: Este programa realiza una auditoría de bajo nivel sobre el hardware,
 * los procesos activos y las tablas de conexión TCP para garantizar que el entorno
 * sea seguro y eficiente.
 */

#include <windows.h>
#include <iostream>
#include <fstream>
#include <psapi.h>
#include <iphlpapi.h>
#include <string>
#include <vector>
#include <memory>

// Vinculación de librerías de red de Windows
#pragma comment(lib, "iphlpapi.lib")
#pragma comment(lib, "ws2_32.lib")

/**
 * FUNCIÓN: AuditarRed
 * Analiza la tabla extendida de conexiones TCP. 
 * Identifica procesos con conexiones a IPs externas (fuera de localhost).
 */
void AuditarRed(std::ofstream& log) {
    DWORD dwSize = 0;
    // Primera llamada para obtener el tamaño necesario del buffer
    GetExtendedTcpTable(NULL, &dwSize, TRUE, AF_INET, TCP_TABLE_OWNER_PID_ALL, 0);
    
    // Uso de std::vector para gestión automática de memoria (RAII)
    std::vector<BYTE> buffer(dwSize);
    PMIB_TCPTABLE_OWNER_PID pTcpTable = reinterpret_cast<PMIB_TCPTABLE_OWNER_PID>(buffer.data());

    log << "[NETWORK_AUDIT] Iniciando escaneo de sockets..." << std::endl;
    
    if (GetExtendedTcpTable(pTcpTable, &dwSize, TRUE, AF_INET, TCP_TABLE_OWNER_PID_ALL, 0) == NO_ERROR) {
        for (DWORD i = 0; i < pTcpTable->dwNumEntries; i++) {
            DWORD remoteAddr = pTcpTable->table[i].dwRemoteAddr;
            
            /**
             * FILTRO DE SEGURIDAD (DOMO):
             * Ignora 0.0.0.0 (Escucha) y 127.0.0.1 (Localhost).
             * 16777343 es la representación decimal de 127.0.0.1 en Little Endian.
             */
            if (remoteAddr != 0 && remoteAddr != 16777343) {
                log << "ALERTA_DOMO | PID: " << pTcpTable->table[i].dwOwningPid 
                    << " | ESTADO: CONEXION_EXTERNA_DETECTADA" << std::endl;
            }
        }
    } else {
        log << "[ERROR] Fallo al acceder a la tabla TCP del sistema." << std::endl;
    }
}

/**
 * FUNCIÓN: TerminarProceso
 * Intenta cerrar un proceso de forma segura mediante su PID.
 */
void TerminarProceso(DWORD pid) {
    // Abrimos el proceso con permisos de terminación
    HANDLE hProcess = OpenProcess(PROCESS_TERMINATE, FALSE, pid);
    if (hProcess != NULL) {
        if (TerminateProcess(hProcess, 0)) {
            std::cout << "[DOMO] PID " << pid << " neutralizado con exito." << std::endl;
        }
        CloseHandle(hProcess);
    } else {
        std::cerr << "[ERROR] Permisos insuficientes para el PID: " << pid << std::endl;
    }
}

/**
 * FUNCIÓN: Main
 * Punto de entrada. Soporta argumentos de comando para acciones rápidas.
 */
int main(int argc, char* argv[]) {
    // Comando rápido: monitor.exe kill <pid>
    if (argc > 2 && std::string(argv[1]) == "kill") {
        TerminarProceso(std::stoul(argv[2]));
        return 0;
    }

    // Apertura de flujo de datos para comunicación con Python
    std::ofstream log("estado_disco.txt", std::ios::trunc);
    if (!log.is_open()) return 1;

    // 1. Auditoría de Memoria Global
    MEMORYSTATUSEX memStatus = { sizeof(memStatus) };
    if (GlobalMemoryStatusEx(&memStatus)) {
        log << "RAM_USO_TOTAL: " << memStatus.dwMemoryLoad << "%" << std::endl;
    }

    // 2. Auditoría de Conexiones (Domo)
    AuditarRed(log);

    // 3. Auditoría de Procesos Pesados
    DWORD processes[1024], cbNeeded;
    if (EnumProcesses(processes, sizeof(processes), &cbNeeded)) {
        DWORD cProcesses = cbNeeded / sizeof(DWORD);
        log << "--- DETECCION_DE_PROCESOS ---" << std::endl;

        for (unsigned int i = 0; i < cProcesses; i++) {
            if (processes[i] == 0) continue;

            // Pedimos permisos de consulta y lectura de memoria
            HANDLE hProcess = OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, FALSE, processes[i]);
            if (hProcess) {
                TCHAR szName[MAX_PATH];
                if (GetModuleBaseName(hProcess, NULL, szName, MAX_PATH)) {
                    PROCESS_MEMORY_COUNTERS pmc;
                    if (GetProcessMemoryInfo(hProcess, &pmc, sizeof(pmc))) {
                        SIZE_T ramMB = pmc.WorkingSetSize / (1024 * 1024);
                        
                        // Solo reportamos si consume más de 150MB para optimizar el log
                        if (ramMB > 150) {
                            log << "PID: " << processes[i] << " | App: " << szName 
                                << " | RAM: " << ramMB << " MB" << std::endl;
                        }
                    }
                }
                CloseHandle(hProcess);
            }
        }
    }

    log.close();
    std::cout << "[SYSTEM] Auditoria completada y reportada al archivo de intercambio." << std::endl;
    return 0;
}