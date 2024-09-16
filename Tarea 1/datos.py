import psycopg2
import pandas as pd
import matplotlib.pyplot as plt

# Conectar a la base de datos PostgreSQL
def connect_postgres():
    try:
        conn = psycopg2.connect(
            dbname="dns_cache",
            user="user",
            password="password",
            host="localhost",  # Cambiado para conectarse desde la máquina local
            port="5432"        # Puerto mapeado desde el contenedor PostgreSQL
        )
        print("Conexión exitosa a PostgreSQL")
        return conn
    except psycopg2.OperationalError as e:
        print(f"Error de conexión a PostgreSQL: {e}")
        return None

# Obtener Hit/Miss rate
def get_hit_miss_rate(conn):
    query = """
    WITH miss_hit_counts AS (
        SELECT 
            result, 
            COUNT(*) AS total_count
        FROM dns_hit_miss
        GROUP BY result
    ),
    dominios_sin_ip AS (
        SELECT COUNT(domain) AS total_sin_ip
        FROM dns_domain_data
        WHERE ip_address = 'No IP found'
    )
    SELECT 
        'MISS' AS hit_rate,
        (mh.total_count - dsi.total_sin_ip) AS cantidad
    FROM miss_hit_counts mh, dominios_sin_ip dsi
    WHERE mh.result = 'MISS'
    
    UNION ALL
    
    SELECT 
        'HIT' AS hit_rate,
        mh.total_count AS cantidad
    FROM miss_hit_counts mh
    WHERE mh.result = 'HIT';
    """
    return pd.read_sql(query, conn)

# Obtener tiempos de respuesta (promedio y desviación estándar)
def get_response_times(conn):
    query = """
    WITH time_diffs AS (
        SELECT partition_number, 
               EXTRACT(EPOCH FROM (timestamp - lag(timestamp) OVER (PARTITION BY partition_number ORDER BY timestamp))) AS response_time
        FROM dns_hit_miss
    )
    SELECT partition_number, 
           AVG(response_time) AS avg_response_time,
           STDDEV(response_time) AS stddev_response_time
    FROM time_diffs
    GROUP BY partition_number;
    """
    return pd.read_sql(query, conn)
    
# Obtener balance de carga (peticiones por partición)
def get_load_balance(conn):
    query = """
    SELECT COUNT(domain) AS dominio, partition_number             
    FROM dns_domain_data                                          
    WHERE dns_domain_data.ip_address != 'No IP found'
    GROUP BY partition_number;
    """
    return pd.read_sql(query, conn)

# Guardar los resultados en un archivo de texto
def save_results_to_txt(hit_miss_rate, response_times, load_balance, filename="results.txt"):
    with open(filename, "w") as file:
        file.write("Hit/Miss Rate:\n")
        file.write(hit_miss_rate.to_string(index=False))
        file.write("\n\n")

        file.write("Tiempos de Respuesta (Promedio y Desviación Estándar):\n")
        file.write(response_times.to_string(index=False))
        file.write("\n\n")

        file.write("Balance de Carga (Peticiones por Partición):\n")
        file.write(load_balance.to_string(index=False))
        file.write("\n\n")

    print(f"Resultados guardados en {filename}")

# Función para generar gráficos
def generate_plots(hit_miss_rate, response_times, load_balance):
    # Gráfico para Hit/Miss Rate
    hit_miss_rate.plot(kind='bar', x='hit_rate', y='cantidad', legend=False, title='Hit/Miss Rate')
    plt.ylabel('Cantidad')
    plt.savefig("hit_miss_rate.png")
    plt.clf()  # Limpiar el gráfico para el siguiente

    # Gráfico combinado para Tiempos de Respuesta (Promedio y Desviación Estándar)
    fig, ax1 = plt.subplots()

    ax1.set_xlabel('Partition Number')
    ax1.set_ylabel('Tiempo promedio (segundos)', color='tab:blue')
    ax1.bar(response_times['partition_number'].to_numpy(), response_times['avg_response_time'].to_numpy(), color='tab:blue', label='Tiempo Promedio')
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    ax2 = ax1.twinx()  # Instanciar un segundo eje que comparte el mismo eje x
    ax2.set_ylabel('Desviación estándar (segundos)', color='tab:red')  
    ax2.plot(response_times['partition_number'].to_numpy(), response_times['stddev_response_time'].to_numpy(), color='tab:red', marker='o', label='Desviación Estándar')
    ax2.tick_params(axis='y', labelcolor='tab:red')

    fig.tight_layout()  # Para que no se superpongan los gráficos
    plt.title("Tiempos de Respuesta (Promedio y Desviación Estándar)")
    plt.savefig("response_times_combined.png")
    plt.clf()

    # Gráfico para Balance de Carga
    load_balance.plot(kind='bar', x='partition_number', y='dominio', legend=False, title='Balance de Carga')
    plt.ylabel('Peticiones')
    plt.savefig("load_balance.png")
    plt.clf()

    print("Gráficos guardados como PNG")

# Función principal
def main():
    conn = connect_postgres()

    if conn:
        # Obtener resultados
        hit_miss_rate = get_hit_miss_rate(conn)
        response_times = get_response_times(conn)
        load_balance = get_load_balance(conn)

        # Guardar resultados en un archivo de texto
        save_results_to_txt(hit_miss_rate, response_times, load_balance)

        # Generar gráficos y guardarlos como PNG
        generate_plots(hit_miss_rate, response_times, load_balance)

        # Cerrar la conexión
        conn.close()

if __name__ == '__main__':
    main()

