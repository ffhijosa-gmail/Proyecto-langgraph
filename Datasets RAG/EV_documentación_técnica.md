# Documento Técnico -- Sistema de Carga para Vehículo Eléctrico EV HyperCharge XG-480 Pro

## 1. Identificación del Producto

**Nombre comercial:** EV HyperCharge XG-480 Pro\
**Código interno de producto:** HCXG-480P-TRI-22-DC50\
**Versión de firmware base:** FW-XG480-3.2.17-RC\
**Revisión de hardware:** Rev. D4.3\
**Año de lanzamiento:** 2026\
**Fabricante hipotético:** HyperGrid Mobility Systems

------------------------------------------------------------------------

## 2. Tipología del Equipo

Sistema de carga híbrido AC/DC para entornos comerciales y estaciones
semi-rápidas.

-   Carga AC trifásica hasta 22 kW
-   Carga DC hasta 50 kW
-   Gestión dinámica de potencia basada en medición trifásica externa

------------------------------------------------------------------------

## 3. Especificaciones Eléctricas -- Entrada

### 3.1 Alimentación AC

-   Tensión nominal: 400 V ±10% (trifásica)
-   Frecuencia: 50 Hz ±1%
-   Corriente máxima por fase: 32 A
-   Potencia máxima absorbida en AC: 22 kW
-   Factor de potencia: ≥ 0.98
-   THDi: \< 3.5%

### 3.2 Protección de Entrada

-   Magnetotérmica recomendada: 4P 40 A curva C
-   Diferencial integrado: Tipo A + 6 mA DC
-   SPD Tipo 2 integrado (Imax 40 kA)

------------------------------------------------------------------------

## 4. Especificaciones -- Salida AC

-   Potencia configurable: 6 / 11 / 22 kW
-   Corriente máxima: 32 A
-   Tensión: 230 V / 400 V
-   Precisión energética: ±1%
-   Conector: Tipo 2 (IEC 62196-2)
-   Cable estándar: 5 m
-   Conductor interno: 6 mm² cobre

------------------------------------------------------------------------

## 5. Especificaciones -- Módulo DC

-   Potencia máxima DC: 50 kW
-   Tensión de salida: 200 -- 920 V
-   Corriente máxima: 125 A
-   Eficiencia pico: 96.8%
-   Ripple: \< 1.5%
-   Protocolo: CCS Combo 2
-   Refrigeración: ventilación forzada + disipador aluminio anodizado

------------------------------------------------------------------------

## 6. Gestión Dinámica de Carga (DLM-X480)

-   Medición trifásica mediante pinza CT-120A
-   Tiempo de respuesta: \< 250 ms
-   Rango potencia contratada configurable: 10 kW -- 63 kW
-   Algoritmo: DLM-ALPHA-3.7-PROPORTIONAL

Modos: - Prioridad Vehículo 1 - Balanceo Equitativo - Protección Red
(\>95% potencia contratada)

------------------------------------------------------------------------

## 7. Conectividad

### Interfaces

-   Ethernet 10/100 Mbps
-   WiFi 2.4 GHz
-   RS485 Modbus RTU
-   USB-C mantenimiento

### Protocolos

-   OCPP 1.6 JSON
-   OCPP 2.0.1
-   Modbus TCP
-   MQTT

### Seguridad

-   TLS 1.3
-   Certificados X.509
-   RFID MIFARE ISO/IEC 14443A
-   BLE 5.0 opcional

------------------------------------------------------------------------

## 8. Componentes Internos

-   Contactores: Schneider LC1D32
-   IMD-480P
-   Placa: HGMB-X480-MAIN-REV3
-   MCU: STM32H743ZI
-   Medición: ADE9153A
-   Sensor temp: NTC 10k ±1%

------------------------------------------------------------------------

## 9. Características Mecánicas

-   Dimensiones: 540 x 320 x 210 mm
-   Peso: 18.6 kg
-   IP54
-   IK10
-   Material: Policarbonato UL94 V-0
-   Temp operación: -25 °C a +50 °C
-   Humedad: 95% sin condensación

------------------------------------------------------------------------

## 10. Refrigeración

-   2 ventiladores 120 mm PWM
-   140 m³/h
-   38 dB(A)
-   Activación \> 42 °C

------------------------------------------------------------------------

## 11. Medición Energética

-   MID Clase B
-   Resolución: 0.01 kWh
-   Registro cada 5 s
-   Almacenamiento local: 30 días

------------------------------------------------------------------------

## 12. Firmware

-   Arquitectura modular
-   FreeRTOS
-   Arranque: 7.8 s
-   Watchdog independiente
-   10.000 eventos internos
-   OTA

------------------------------------------------------------------------

## 13. Seguridad Funcional

-   Detección soldadura contactores
-   Monitorización temperatura cable
-   Corte ante fuga DC \> 6 mA
-   Diagnóstico cada 60 s

------------------------------------------------------------------------

## 14. Rendimiento

-   MTBF: 85.000 h

-   100.000 ciclos contactor

-   EN 61000-6-3

-   IEC 61851-1

------------------------------------------------------------------------

## 15. Parámetros Específicos para Validación RAG

-   Tensión mínima activación DC: 214 V
-   Tiempo estabilización tras pico: 1.35 s
-   Umbral térmico reducción progresiva: 47.5 °C
-   Identificador módulo DC: DCX-920-125A-REV2
