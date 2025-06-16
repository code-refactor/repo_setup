"""
Relationship management and graph utilities for the unified personal knowledge management library.
"""

from collections import defaultdict, deque
from typing import Any, Dict, List, Optional, Set, Tuple, TypeVar
from uuid import UUID

try:
    import networkx as nx
    HAS_NETWORKX = True
except ImportError:
    HAS_NETWORKX = False

from .models import BaseKnowledgeNode, BaseRelationship
from .storage import BaseStorage

T = TypeVar('T', bound=BaseKnowledgeNode)


class RelationshipManager:
    """
    Manager for handling relationships between knowledge entities.
    """
    
    def __init__(self, storage: BaseStorage):
        self.storage = storage
        self._graph = None
        self._graph_dirty = True
    
    def add_relationship(self, source_id: UUID, target_id: UUID, relationship_type: str, 
                        metadata: Optional[Dict[str, Any]] = None) -> BaseRelationship:
        """Add a relationship between two entities."""
        relationship = BaseRelationship(
            source_id=source_id,
            target_id=target_id,
            relationship_type=relationship_type,
            metadata=metadata or {}
        )
        
        self.storage.save(relationship)
        self._graph_dirty = True
        return relationship
    
    def get_relationships(self, entity_id: UUID, relationship_type: Optional[str] = None,
                         direction: str = 'both') -> List[BaseRelationship]:
        """Get relationships for an entity."""
        all_relationships = self.storage.get_all(BaseRelationship)
        
        filtered_relationships = []
        for rel in all_relationships:
            if relationship_type and rel.relationship_type != relationship_type:
                continue
            
            if direction == 'outgoing' and rel.source_id == entity_id:
                filtered_relationships.append(rel)
            elif direction == 'incoming' and rel.target_id == entity_id:
                filtered_relationships.append(rel)
            elif direction == 'both' and (rel.source_id == entity_id or rel.target_id == entity_id):
                filtered_relationships.append(rel)
        
        return filtered_relationships
    
    def get_related_entities(self, entity_id: UUID, relationship_type: Optional[str] = None,
                           direction: str = 'both', max_depth: int = 1) -> List[UUID]:
        """Get IDs of entities related to the given entity."""
        if max_depth <= 0:
            return []
        
        visited = set()
        to_visit = [(entity_id, 0)]
        related_entities = []
        
        while to_visit:
            current_id, depth = to_visit.pop(0)
            
            if current_id in visited or depth >= max_depth:
                continue
            
            visited.add(current_id)
            
            # Get direct relationships
            relationships = self.get_relationships(current_id, relationship_type, direction)
            
            for rel in relationships:
                if rel.source_id == current_id:
                    related_id = rel.target_id
                else:
                    related_id = rel.source_id
                
                if related_id not in visited:
                    related_entities.append(related_id)
                    if depth + 1 < max_depth:
                        to_visit.append((related_id, depth + 1))
        
        return list(set(related_entities))  # Remove duplicates
    
    def remove_relationship(self, relationship_id: UUID) -> bool:
        """Remove a relationship."""
        success = self.storage.delete(BaseRelationship, relationship_id)
        if success:
            self._graph_dirty = True
        return success
    
    def get_relationship_counts(self, entity_id: UUID) -> Dict[str, int]:
        """Get counts of relationships by type for an entity."""
        relationships = self.get_relationships(entity_id)
        counts = defaultdict(int)
        
        for rel in relationships:
            counts[rel.relationship_type] += 1
        
        return dict(counts)


class GraphUtils:
    """
    Utilities for graph-based operations on knowledge entities.
    Provides a simple graph implementation if NetworkX is not available.
    """
    
    def __init__(self, storage: BaseStorage):
        self.storage = storage
        self.use_networkx = HAS_NETWORKX
    
    def build_graph(self, entities: Optional[List[T]] = None, 
                   relationships: Optional[List[BaseRelationship]] = None) -> Any:
        """Build a graph from entities and relationships."""
        if self.use_networkx:
            return self._build_networkx_graph(entities, relationships)
        else:
            return self._build_simple_graph(entities, relationships)
    
    def _build_networkx_graph(self, entities: Optional[List[T]] = None,
                             relationships: Optional[List[BaseRelationship]] = None) -> nx.DiGraph:
        """Build a NetworkX graph."""
        graph = nx.DiGraph()
        
        # Add nodes
        if entities:
            for entity in entities:
                graph.add_node(entity.id, **entity.metadata)
        
        # Add edges
        if relationships:
            for rel in relationships:
                graph.add_edge(
                    rel.source_id,
                    rel.target_id,
                    relationship_type=rel.relationship_type,
                    **rel.metadata
                )
        
        return graph
    
    def _build_simple_graph(self, entities: Optional[List[T]] = None,
                           relationships: Optional[List[BaseRelationship]] = None) -> Dict[str, Any]:
        """Build a simple graph representation."""
        graph = {
            'nodes': {},
            'edges': defaultdict(list)
        }
        
        # Add nodes
        if entities:
            for entity in entities:
                graph['nodes'][entity.id] = entity.metadata
        
        # Add edges
        if relationships:
            for rel in relationships:
                edge_data = {
                    'target': rel.target_id,
                    'relationship_type': rel.relationship_type,
                    'metadata': rel.metadata
                }
                graph['edges'][rel.source_id].append(edge_data)
        
        return graph
    
    def find_shortest_path(self, graph: Any, source: UUID, target: UUID) -> Optional[List[UUID]]:
        """Find shortest path between two nodes."""
        if self.use_networkx and isinstance(graph, nx.DiGraph):
            try:
                path = nx.shortest_path(graph, source, target)
                return path
            except nx.NetworkXNoPath:
                return None
        else:
            return self._find_shortest_path_simple(graph, source, target)
    
    def _find_shortest_path_simple(self, graph: Dict[str, Any], source: UUID, target: UUID) -> Optional[List[UUID]]:
        """Find shortest path using BFS in simple graph."""
        if source == target:
            return [source]
        
        queue = deque([(source, [source])])
        visited = {source}
        
        while queue:
            current, path = queue.popleft()
            
            # Get neighbors
            for edge in graph['edges'].get(current, []):
                neighbor = edge['target']
                
                if neighbor == target:
                    return path + [neighbor]
                
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return None
    
    def get_connected_components(self, graph: Any) -> List[List[UUID]]:
        """Get connected components of the graph."""
        if self.use_networkx and isinstance(graph, nx.DiGraph):
            # Convert to undirected for connected components
            undirected = graph.to_undirected()
            return [list(component) for component in nx.connected_components(undirected)]
        else:
            return self._get_connected_components_simple(graph)
    
    def _get_connected_components_simple(self, graph: Dict[str, Any]) -> List[List[UUID]]:
        """Get connected components using DFS in simple graph."""
        visited = set()
        components = []
        
        def dfs(node: UUID, component: List[UUID]):
            if node in visited:
                return
            visited.add(node)
            component.append(node)
            
            # Visit outgoing edges
            for edge in graph['edges'].get(node, []):
                dfs(edge['target'], component)
            
            # Visit incoming edges (simulate undirected)
            for source_node, edges in graph['edges'].items():
                for edge in edges:
                    if edge['target'] == node:
                        dfs(source_node, component)
        
        for node in graph['nodes']:
            if node not in visited:
                component = []
                dfs(node, component)
                if component:
                    components.append(component)
        
        return components
    
    def calculate_centrality(self, graph: Any, centrality_type: str = 'degree') -> Dict[UUID, float]:
        """Calculate centrality measures for nodes."""
        if self.use_networkx and isinstance(graph, nx.DiGraph):
            if centrality_type == 'degree':
                return nx.degree_centrality(graph)
            elif centrality_type == 'betweenness':
                return nx.betweenness_centrality(graph)
            elif centrality_type == 'closeness':
                return nx.closeness_centrality(graph)
            elif centrality_type == 'pagerank':
                return nx.pagerank(graph)
        
        # Simple degree centrality for simple graph
        return self._calculate_degree_centrality_simple(graph)
    
    def _calculate_degree_centrality_simple(self, graph: Dict[str, Any]) -> Dict[UUID, float]:
        """Calculate degree centrality for simple graph."""
        degree_counts = defaultdict(int)
        
        # Count outgoing edges
        for source, edges in graph['edges'].items():
            degree_counts[source] += len(edges)
        
        # Count incoming edges
        for edges in graph['edges'].values():
            for edge in edges:
                degree_counts[edge['target']] += 1
        
        # Normalize by total possible connections
        num_nodes = len(graph['nodes'])
        if num_nodes <= 1:
            return {}
        
        max_degree = num_nodes - 1
        centrality = {}
        for node in graph['nodes']:
            centrality[node] = degree_counts[node] / max_degree
        
        return centrality
    
    def detect_cycles(self, graph: Any) -> List[List[UUID]]:
        """Detect cycles in the graph."""
        if self.use_networkx and isinstance(graph, nx.DiGraph):
            try:
                cycles = list(nx.simple_cycles(graph))
                return cycles
            except:
                return []
        else:
            return self._detect_cycles_simple(graph)
    
    def _detect_cycles_simple(self, graph: Dict[str, Any]) -> List[List[UUID]]:
        """Detect cycles using DFS in simple graph."""
        visited = set()
        rec_stack = set()
        cycles = []
        
        def dfs(node: UUID, path: List[UUID]):
            if node in rec_stack:
                # Found a cycle
                cycle_start = path.index(node)
                cycles.append(path[cycle_start:] + [node])
                return
            
            if node in visited:
                return
            
            visited.add(node)
            rec_stack.add(node)
            
            for edge in graph['edges'].get(node, []):
                dfs(edge['target'], path + [node])
            
            rec_stack.remove(node)
        
        for node in graph['nodes']:
            if node not in visited:
                dfs(node, [])
        
        return cycles


class ConnectionTracker:
    """
    Tracks and analyzes connections between entities.
    """
    
    def __init__(self, storage: BaseStorage):
        self.storage = storage
        self.relationship_manager = RelationshipManager(storage)
        self.graph_utils = GraphUtils(storage)
    
    def analyze_entity_connections(self, entity_id: UUID) -> Dict[str, Any]:
        """Analyze connections for a specific entity."""
        relationships = self.relationship_manager.get_relationships(entity_id)
        
        analysis = {
            'entity_id': str(entity_id),
            'total_relationships': len(relationships),
            'relationship_types': self.relationship_manager.get_relationship_counts(entity_id),
            'connected_entities': len(self.relationship_manager.get_related_entities(entity_id)),
            'relationship_details': []
        }
        
        for rel in relationships:
            analysis['relationship_details'].append({
                'id': str(rel.id),
                'type': rel.relationship_type,
                'direction': 'outgoing' if rel.source_id == entity_id else 'incoming',
                'connected_entity': str(rel.target_id if rel.source_id == entity_id else rel.source_id),
                'metadata': rel.metadata,
                'created_at': rel.created_at.isoformat()
            })
        
        return analysis
    
    def find_connection_paths(self, source_id: UUID, target_id: UUID) -> List[List[UUID]]:
        """Find all paths between two entities."""
        # Build graph with all relationships
        relationships = self.storage.get_all(BaseRelationship)
        graph = self.graph_utils.build_graph(relationships=relationships)
        
        # For simple implementation, just find shortest path
        path = self.graph_utils.find_shortest_path(graph, source_id, target_id)
        return [path] if path else []
    
    def suggest_connections(self, entity_id: UUID, max_suggestions: int = 5) -> List[Dict[str, Any]]:
        """Suggest potential connections based on existing patterns."""
        # Get entities connected to this entity
        related_entities = self.relationship_manager.get_related_entities(entity_id, max_depth=2)
        
        # Count common connections
        connection_counts = defaultdict(int)
        for related_id in related_entities:
            second_level = self.relationship_manager.get_related_entities(related_id, max_depth=1)
            for candidate_id in second_level:
                if candidate_id != entity_id:
                    connection_counts[candidate_id] += 1
        
        # Sort by connection strength and return top suggestions
        suggestions = []
        for candidate_id, strength in sorted(connection_counts.items(), 
                                           key=lambda x: x[1], reverse=True)[:max_suggestions]:
            suggestions.append({
                'entity_id': str(candidate_id),
                'connection_strength': strength,
                'common_connections': strength
            })
        
        return suggestions
    
    def get_network_statistics(self) -> Dict[str, Any]:
        """Get overall network statistics."""
        relationships = self.storage.get_all(BaseRelationship)
        
        if not relationships:
            return {'total_relationships': 0}
        
        # Build graph for analysis
        graph = self.graph_utils.build_graph(relationships=relationships)
        
        # Calculate basic statistics
        relationship_types = defaultdict(int)
        entities = set()
        
        for rel in relationships:
            relationship_types[rel.relationship_type] += 1
            entities.add(rel.source_id)
            entities.add(rel.target_id)
        
        stats = {
            'total_relationships': len(relationships),
            'unique_entities': len(entities),
            'relationship_types': dict(relationship_types),
            'average_connections_per_entity': len(relationships) * 2 / len(entities) if entities else 0
        }
        
        # Add graph-specific statistics
        if HAS_NETWORKX and hasattr(graph, 'number_of_nodes'):
            stats['connected_components'] = len(self.graph_utils.get_connected_components(graph))
            stats['cycles'] = len(self.graph_utils.detect_cycles(graph))
        
        return stats