import pandas as pd
import numpy as np
import os
import json
from datetime import datetime

def main():
    print("--- Iniciando Pipeline Big Data: Proyecto Paralelo (Runners) ---")
    timestamp_ejecucion = datetime.now().isoformat()
    linaje = {"ejecucion": timestamp_ejecucion, "pasos": []}

    # ---------------------------------------------------------
    # 1. ZONA BRONZE (Ingesta de datos crudos simulados)
    # ---------------------------------------------------------
    print("[*] Zona Bronze: Generando ingesta de cruces Bluetooth...")
    # Simulamos 100,000 eventos de cruce entre corredores
    N = 100000
    datos_crudos = pd.DataFrame({
        'id_cruce': range(1, N + 1),
        'id_runner_A': np.random.randint(100, 200, N),
        'id_runner_B': np.random.randint(100, 200, N),
        'senal_rssi': np.random.uniform(-110, -30, N), # Fuerza de señal Bluetooth
        'latitud': np.random.uniform(-33.6, -33.4, N), # Zona La Florida
        'longitud': np.random.uniform(-70.7, -70.5, N),
        'fecha_hora': [datetime.now().strftime("%Y-%m-%d %H:%M:%S") for _ in range(N)],
        'estado_cruce': np.random.choice(['exito', 'fallo', None], N, p=[0.8, 0.15, 0.05])
    })
    
    # Inyectamos errores intencionales para probar las reglas de calidad
    datos_crudos.loc[10:20, 'id_runner_A'] = datos_crudos.loc[10:20, 'id_runner_B'] # Mismo ID
    datos_crudos.loc[50:60, 'senal_rssi'] = 10 # RSSI imposible (positivo)

    ruta_bronze = '/app/bronze/cruces_raw.csv'
    datos_crudos.to_csv(ruta_bronze, index=False)
    linaje["pasos"].append({"fase": "Ingesta Bronze", "registros": N, "archivo": ruta_bronze})

    # ---------------------------------------------------------
    # 2. CALIDAD DE DATOS Y ZONA SILVER (Limpieza)
    # ---------------------------------------------------------
    print("[*] Zona Silver: Aplicando Reglas de Calidad...")
    df = pd.read_csv(ruta_bronze)
    
    reporte_calidad = {
        "total_leido": len(df),
        "reglas_fallidas": {}
    }

    # Regla 1: Nulos en estado (Completitud)
    nulos = df['estado_cruce'].isnull().sum()
    reporte_calidad["reglas_fallidas"]["estado_nulo"] = int(nulos)
    df = df.dropna(subset=['estado_cruce'])

    # Regla 2: Runner A no puede ser igual a Runner B (Consistencia)
    mismo_id = (df['id_runner_A'] == df['id_runner_B']).sum()
    reporte_calidad["reglas_fallidas"]["mismo_runner"] = int(mismo_id)
    df = df[df['id_runner_A'] != df['id_runner_B']]

    # Regla 3: RSSI debe ser negativo (Rango Lógico)
    rssi_invalido = (df['senal_rssi'] >= 0).sum()
    reporte_calidad["reglas_fallidas"]["rssi_invalido"] = int(rssi_invalido)
    df = df[df['senal_rssi'] < 0]

    # Guardamos el dataset limpio en Parquet (Almacenamiento Columnar)
    ruta_silver = '/app/silver/cruces_clean.parquet'
    df.to_parquet(ruta_silver, engine='pyarrow', index=False)
    linaje["pasos"].append({"fase": "Limpieza Silver", "registros_finales": len(df), "archivo": ruta_silver})

    # ---------------------------------------------------------
    # 3. ZONA GOLD (Agregación Analítica)
    # ---------------------------------------------------------
    print("[*] Zona Gold: Generando métricas analíticas...")
    # ¿Qué runner generó más "choques de cinco" virtuales?
    metricas = df[df['estado_cruce'] == 'exito'].groupby('id_runner_A').size().reset_index(name='total_interacciones')
    metricas = metricas.sort_values(by='total_interacciones', ascending=False)
    
    ruta_gold = '/app/gold/ranking_runners.parquet'
    metricas.to_parquet(ruta_gold, engine='pyarrow', index=False)
    linaje["pasos"].append({"fase": "Métricas Gold", "archivo": ruta_gold})

    # ---------------------------------------------------------
    # 4. EXPORTAR METADATOS Y LINAJE
    # ---------------------------------------------------------
    print("[*] Guardando Reportes de Calidad y Linaje...")
    with open('/app/metrics/reporte_calidad.json', 'w') as f:
        json.dump(reporte_calidad, f, indent=4)
        
    with open('/app/metadata/linaje.json', 'w') as f:
        json.dump(linaje, f, indent=4)

    print("\n[OK] Pipeline Finalizado con Éxito. Zonas actualizadas.")
    print(f"-> Registros iniciales: {reporte_calidad['total_leido']}")
    print(f"-> Registros descartados por reglas de calidad: {sum(reporte_calidad['reglas_fallidas'].values())}")

if __name__ == "__main__":
    # Eliminamos la creación forzada de carpetas para evitar conflictos con los volúmenes de Docker
    main()