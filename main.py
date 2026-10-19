import os
from grafos import (grafoMalla, grafoErdosRenyi, grafoGilbert, 
                    grafoGeografico, grafoBarabasiAlbert, grafoDorogovtsevMendes)

def ejecutar_tarea_2():
    dir_generados = "output_gv/generados"
    dir_calculados = "output_gv/calculados"
    os.makedirs(dir_generados, exist_ok=True)
    os.makedirs(dir_calculados, exist_ok=True)
    
    # Tamaños requeridos por la especificación de la Tarea 2
    tamanos = [30, 100, 500]
    dimensiones_malla = {30: (6, 5), 100: (10, 10), 500: (25, 20)}
    
    for n in tamanos:
        print(f"\n--- Generando y calculando grafos de {n} nodos ---")
        
        m, cols = dimensiones_malla[n]
        # Parámetros ajustados para garantizar suficiente conectividad en el recorrido
        p_gilbert = 0.15 if n == 30 else (0.05 if n == 100 else 0.015)
        r_geo = 0.3 if n == 30 else (0.15 if n == 100 else 0.08)
        
        modelos = {
            "malla": grafoMalla(m, cols),
            "erdos_renyi": grafoErdosRenyi(n, n * 2),
            "gilbert": grafoGilbert(n, p_gilbert),
            "geografico": grafoGeografico(n, r_geo),
            "barabasi": grafoBarabasiAlbert(n, 4),
            "dorogovtsev": grafoDorogovtsevMendes(n)
        }
        
        for nombre, grafo in modelos.items():
            # 1. Guardar grafo original generado
            archivo_original = f"{dir_generados}/{nombre}_{n}.gv"
            grafo.guardar_graphviz(archivo_original)
            print(f"[OK] Generado: {archivo_original}")
            
            # 2. Selección de nodo fuente s
            s = "n_0_0" if "n_0_0" in grafo.nodos else "0"
            
            # 3. Cálculo de los árboles inducidos
            arbol_bfs = grafo.BFS(s)
            arbol_dfs_r = grafo.DFS_R(s)
            arbol_dfs_i = grafo.DFS_I(s)
            
            # 4. Guardar árboles calculados
            arbol_bfs.guardar_graphviz(f"{dir_calculados}/{nombre}_{n}_bfs.gv")
            arbol_dfs_r.guardar_graphviz(f"{dir_calculados}/{nombre}_{n}_dfs_r.gv")
            arbol_dfs_i.guardar_graphviz(f"{dir_calculados}/{nombre}_{n}_dfs_i.gv")
            print(f"     └─ Calculados BFS, DFS_R y DFS_I para {nombre}_{n}")

if __name__ == '__main__':
    ejecutar_tarea_2()
    print("\n¡Listo! Se han generado los 72 archivos .gv en la carpeta 'output_gv'.")