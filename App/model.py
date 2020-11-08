"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * Contribución de:
 *
 * Dario Correal
 *
 """
import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
assert config

"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""

# -----------------------------------------------------
#                       API
# -----------------------------------------------------

def newAnalyzer():
    """ Inicializa el analizador
   graph: Grafo para representar las estaciones
    """
    try:
        analyzer = {
                  'graph': None
                   }
        analyzer['graph'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000,
                                              comparefunction=compareStations)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')

# Funciones para agregar informacion al grafo

def addTrip(analyzer, trip):
    try:
        origin = trip["start station id"]
        destination = trip["end station id"]
        duration = int(trip["tripduration"])
        addStation(analyzer, origin)
        addStation(analyzer, destination)
        addConnection(analyzer, origin, destination, duration)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addTrip')

def addStation(analyzer, stationid):
    """
    Adiciona una estación como un vertice del grafo
    """
    try:
        if not gr.containsVertex(analyzer['graph'], stationid):
            gr.insertVertex(analyzer['graph'], stationid)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addStation')

def addConnection(analyzer, origin, destination, duration):
    """
    Adiciona un arco entre dos estaciones
    """
    edge = gr.getEdge(analyzer['graph'], origin, destination)
    if edge is None:
        gr.addEdge(analyzer['graph'], origin, destination, duration)
    return analyzer        

# ==============================
# Funciones de consulta
# ==============================

def totalStations(analyzer):
    """
    Retorna el total de estaciones (vertices) del grafo
    """
    return gr.numVertices(analyzer['graph'])


def totalConnections(analyzer):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(analyzer['graph'])

def strongComponents(graph):
    return scc.KosarajuSCC(graph)

def numSCC(sc):
    return scc.connectedComponents(sc)

def sameCC(sc, station1, station2):    
    return scc.stronglyConnected(sc, station1, station2)    
    
# ==============================
# Funciones Helper
# ==============================

# ==============================
# Funciones de Comparacion
# ==============================

def compareStations(station1, station2):
    """
    Compara dos estaciones
    """
    station2 = station2["key"]
    if (station1 == station2):
        return 0
    elif (station1 > station2):
        return 1
    else:
        return -1