"""
Decision Registry - System for capturing decision rationale.

This module provides capabilities for:
- Structured decision documentation with standardized attributes
- Context preservation for historical understanding
- Alternative tracking with evaluation criteria
- Outcome prediction and post-implementation assessment
- Cross-reference linking between related decisions
"""
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Optional, Set, Tuple, Union
import json
import os
import re

from productmind.models import (
    Alternative,
    Decision
)


class DecisionRegistry:
    """
    Registry for documenting product decisions with context and rationale.
    
    This class provides methods to:
    - Document decisions with standardized attributes
    - Track alternatives considered with evaluation criteria
    - Preserve context for historical understanding
    - Link related decisions for traceability
    - Record and assess outcomes of decisions
    """
    
    def __init__(self, storage_dir: str = "./data"):
        """
        Initialize the decision registry.
        
        Args:
            storage_dir: Directory to store decision data
        """
        self.storage_dir = storage_dir
        self._decisions_cache = {}
        
        # Create storage directory
        os.makedirs(os.path.join(storage_dir, "decisions"), exist_ok=True)
    
    def add_decision(self, decision: Union[Decision, List[Decision]]) -> List[str]:
        """
        Add a new decision or list of decisions to the registry.
        
        Args:
            decision: Decision or list of decisions to add
            
        Returns:
            List of decision IDs
        """
        if isinstance(decision, Decision):
            decision = [decision]
        
        decision_ids = []
        for item in decision:
            self._store_decision(item)
            decision_ids.append(str(item.id))
        
        return decision_ids
    
    def _store_decision(self, decision: Decision) -> None:
        """
        Store a decision in cache and on disk.
        
        Args:
            decision: Decision to store
        """
        # Store in memory cache
        self._decisions_cache[str(decision.id)] = decision
        
        # Store on disk
        decision_path = os.path.join(
            self.storage_dir, "decisions", f"{decision.id}.json"
        )
        with open(decision_path, "w") as f:
            f.write(decision.model_dump_json())
    
    def get_decision(self, decision_id: str) -> Optional[Decision]:
        """
        Retrieve a decision by ID.
        
        Args:
            decision_id: ID of the decision to retrieve
            
        Returns:
            Decision if found, None otherwise
        """
        # Try to get from cache first
        if decision_id in self._decisions_cache:
            return self._decisions_cache[decision_id]
        
        # Try to load from disk
        decision_path = os.path.join(
            self.storage_dir, "decisions", f"{decision_id}.json"
        )
        if os.path.exists(decision_path):
            with open(decision_path, "r") as f:
                decision_data = json.load(f)
                decision = Decision.model_validate(decision_data)
                self._decisions_cache[decision_id] = decision
                return decision
        
        return None
    
    def get_all_decisions(self) -> List[Decision]:
        """
        Retrieve all decisions.
        
        Returns:
            List of all decisions
        """
        decisions = []
        decisions_dir = os.path.join(self.storage_dir, "decisions")
        
        if not os.path.exists(decisions_dir):
            return decisions
        
        for filename in os.listdir(decisions_dir):
            if filename.endswith(".json"):
                decision_id = filename.replace(".json", "")
                decision = self.get_decision(decision_id)
                if decision:
                    decisions.append(decision)
        
        return decisions
    
    def add_alternative_to_decision(
        self, 
        decision_id: str, 
        alternative: Alternative
    ) -> Decision:
        """
        Add an alternative to an existing decision.
        
        Args:
            decision_id: ID of the decision
            alternative: Alternative to add
            
        Returns:
            Updated decision
        """
        decision = self.get_decision(decision_id)
        if not decision:
            raise ValueError(f"Decision with ID {decision_id} not found")
        
        # Check if alternative already exists by name
        for existing_alt in decision.alternatives:
            if existing_alt.name == alternative.name:
                raise ValueError(f"Alternative with name '{alternative.name}' already exists")
        
        # Add alternative
        decision.alternatives.append(alternative)
        decision.updated_at = datetime.now()
        
        # Save decision
        self._store_decision(decision)
        
        return decision
    
    def link_related_decisions(
        self, 
        decision_id: str, 
        related_decision_ids: List[str]
    ) -> Decision:
        """
        Link related decisions to a decision.
        
        Args:
            decision_id: ID of the decision
            related_decision_ids: IDs of related decisions
            
        Returns:
            Updated decision
        """
        decision = self.get_decision(decision_id)
        if not decision:
            raise ValueError(f"Decision with ID {decision_id} not found")
        
        # Verify all related decisions exist
        for related_id in related_decision_ids:
            related_decision = self.get_decision(related_id)
            if not related_decision:
                raise ValueError(f"Related decision with ID {related_id} not found")
        
        # Update related decisions
        for related_id in related_decision_ids:
            if related_id != decision_id and related_id not in decision.related_decisions:
                decision.related_decisions.append(related_id)
                
                # Also link in the other direction
                related_decision = self.get_decision(related_id)
                if decision_id not in related_decision.related_decisions:
                    related_decision.related_decisions.append(decision_id)
                    related_decision.updated_at = datetime.now()
                    self._store_decision(related_decision)
        
        decision.updated_at = datetime.now()
        
        # Save decision
        self._store_decision(decision)
        
        return decision
    
    def record_outcome_assessment(
        self, 
        decision_id: str, 
        outcome_assessment: str
    ) -> Decision:
        """
        Record outcome assessment for a decision.
        
        Args:
            decision_id: ID of the decision
            outcome_assessment: Assessment of the decision outcome
            
        Returns:
            Updated decision
        """
        decision = self.get_decision(decision_id)
        if not decision:
            raise ValueError(f"Decision with ID {decision_id} not found")
        
        # Update outcome assessment
        decision.outcome_assessment = outcome_assessment
        decision.status = "assessed"
        decision.updated_at = datetime.now()
        
        # Save decision
        self._store_decision(decision)
        
        return decision
    
    def search_decisions(
        self, 
        query: str,
        search_fields: Optional[List[str]] = None
    ) -> List[Decision]:
        """
        Search for decisions matching a query.
        
        Args:
            query: Search query
            search_fields: Fields to search (if None, search all text fields)
            
        Returns:
            List of matching decisions
        """
        decisions = self.get_all_decisions()
        results = []
        
        if not search_fields:
            search_fields = ["title", "description", "context", "problem_statement", "rationale"]
        
        query = query.lower()
        
        for decision in decisions:
            for field in search_fields:
                if hasattr(decision, field):
                    field_value = getattr(decision, field)
                    if isinstance(field_value, str) and query in field_value.lower():
                        results.append(decision)
                        break
        
        return results
    
    def get_decision_history(self, filter_by: Optional[Dict] = None) -> List[Dict]:
        """
        Get decision history, optionally filtered.
        
        Args:
            filter_by: Dictionary of filters to apply
            
        Returns:
            List of decisions with summary information
        """
        decisions = self.get_all_decisions()
        
        # Apply filters if provided
        if filter_by:
            filtered_decisions = []
            for decision in decisions:
                include = True
                
                for key, value in filter_by.items():
                    if hasattr(decision, key):
                        attr_value = getattr(decision, key)
                        
                        # Handle list fields
                        if isinstance(attr_value, list) and isinstance(value, str):
                            if value not in attr_value:
                                include = False
                                break
                        # Handle string fields
                        elif isinstance(attr_value, str) and isinstance(value, str):
                            if value.lower() not in attr_value.lower():
                                include = False
                                break
                        # Handle exact match fields
                        elif attr_value != value:
                            include = False
                            break
                
                if include:
                    filtered_decisions.append(decision)
            
            decisions = filtered_decisions
        
        # Sort by decision date
        decisions.sort(key=lambda d: d.decision_date, reverse=True)
        
        # Create summary information
        history = []
        for decision in decisions:
            history.append({
                "id": str(decision.id),
                "title": decision.title,
                "decision_date": decision.decision_date,
                "decision_maker": decision.decision_maker,
                "chosen_alternative": self._get_alternative_name(decision, decision.chosen_alternative),
                "status": decision.status,
                "num_alternatives": len(decision.alternatives),
                "has_outcome_assessment": decision.outcome_assessment is not None,
                "related_decisions": len(decision.related_decisions)
            })
        
        return history
    
    def _get_alternative_name(self, decision: Decision, alternative_id: str) -> str:
        """
        Get the name of an alternative by ID.
        
        Args:
            decision: Decision containing the alternative
            alternative_id: ID of the alternative
            
        Returns:
            Name of the alternative or "Unknown"
        """
        for alt in decision.alternatives:
            if str(alt.id) == alternative_id:
                return alt.name
        
        return "Unknown"
    
    def build_decision_graph(self) -> Dict:
        """
        Build a graph of related decisions.
        
        Returns:
            Dictionary with graph data
        """
        decisions = self.get_all_decisions()
        
        # Create nodes and edges
        nodes = []
        edges = []
        
        for decision in decisions:
            # Add node
            nodes.append({
                "id": str(decision.id),
                "label": decision.title,
                "date": decision.decision_date.isoformat(),
                "status": decision.status
            })
            
            # Add edges
            for related_id in decision.related_decisions:
                # Only add edge if related decision exists
                related_decision = self.get_decision(related_id)
                if related_decision:
                    edge = {
                        "source": str(decision.id),
                        "target": related_id
                    }
                    
                    # Check if edge already exists in reverse direction
                    reverse_edge = {
                        "source": related_id,
                        "target": str(decision.id)
                    }
                    
                    if reverse_edge not in edges:
                        edges.append(edge)
        
        return {
            "nodes": nodes,
            "edges": edges
        }
    
    def analyze_alternatives(self, decision_id: str) -> Dict:
        """
        Analyze alternatives for a decision.
        
        Args:
            decision_id: ID of the decision
            
        Returns:
            Dictionary with analysis results
        """
        decision = self.get_decision(decision_id)
        if not decision:
            raise ValueError(f"Decision with ID {decision_id} not found")
        
        if not decision.alternatives:
            return {
                "decision_id": decision_id,
                "alternatives": [],
                "chosen_alternative": None,
                "score_range": {"min": 0, "max": 0},
                "cost_range": {"min": 0, "max": 0},
                "benefit_range": {"min": 0, "max": 0},
                "risk_range": {"min": 0, "max": 0}
            }
        
        # Analyze alternatives
        alternatives = []
        min_score = float('inf')
        max_score = float('-inf')
        min_cost = float('inf')
        max_cost = float('-inf')
        min_benefit = float('inf')
        max_benefit = float('-inf')
        min_risk = float('inf')
        max_risk = float('-inf')
        
        for alt in decision.alternatives:
            # Calculate normalized metrics for visualization
            score = alt.score if alt.score is not None else 0
            cost = alt.estimated_cost if alt.estimated_cost is not None else 0
            benefit = alt.estimated_benefit if alt.estimated_benefit is not None else 0
            risk = alt.estimated_risk if alt.estimated_risk is not None else 0
            
            # Update ranges
            min_score = min(min_score, score)
            max_score = max(max_score, score)
            min_cost = min(min_cost, cost)
            max_cost = max(max_cost, cost)
            min_benefit = min(min_benefit, benefit)
            max_benefit = max(max_benefit, benefit)
            min_risk = min(min_risk, risk)
            max_risk = max(max_risk, risk)
            
            # Format for output
            alternatives.append({
                "id": str(alt.id),
                "name": alt.name,
                "score": score,
                "cost": cost,
                "benefit": benefit,
                "risk": risk,
                "pros_count": len(alt.pros),
                "cons_count": len(alt.cons),
                "is_chosen": str(alt.id) == str(decision.chosen_alternative)
            })
        
        # Handle edge case of only one alternative
        if min_score == max_score:
            min_score = 0
        if min_cost == max_cost:
            min_cost = 0
        if min_benefit == max_benefit:
            min_benefit = 0
        if min_risk == max_risk:
            min_risk = 0
        
        # Get chosen alternative details
        chosen_alternative = None
        for alt in alternatives:
            if alt["is_chosen"]:
                chosen_alternative = alt
        
        return {
            "decision_id": decision_id,
            "alternatives": alternatives,
            "chosen_alternative": chosen_alternative,
            "score_range": {"min": min_score, "max": max_score},
            "cost_range": {"min": min_cost, "max": max_cost},
            "benefit_range": {"min": min_benefit, "max": max_benefit},
            "risk_range": {"min": min_risk, "max": max_risk}
        }
    
    def generate_decision_template(self, template_type: str = "standard") -> Dict:
        """
        Generate a decision template.
        
        Args:
            template_type: Type of template ("standard", "urgent", "technical", "strategic")
            
        Returns:
            Dictionary with template fields
        """
        # Common fields for all templates
        template = {
            "title": "",
            "description": "",
            "context": "",
            "problem_statement": "",
            "decision_date": datetime.now(),
            "decision_maker": "",
            "alternatives": [],
            "rationale": "",
            "success_criteria": [],
            "status": "proposed"
        }
        
        # Add template-specific fields
        if template_type == "urgent":
            template["context"] = "URGENT DECISION: \n\nBackground: \n\nConstraints: \n\nTimeline: "
            template["problem_statement"] = "Urgent issue requiring immediate decision: "
            template["alternatives"] = [
                {
                    "name": "Option 1",
                    "description": "",
                    "pros": ["Quick to implement"],
                    "cons": ["May have long-term drawbacks"],
                    "estimated_cost": None,
                    "estimated_benefit": None,
                    "estimated_risk": None
                },
                {
                    "name": "Option 2",
                    "description": "",
                    "pros": [],
                    "cons": [],
                    "estimated_cost": None,
                    "estimated_benefit": None,
                    "estimated_risk": None
                }
            ]
            template["success_criteria"] = ["Issue resolved within timeline"]
        
        elif template_type == "technical":
            template["context"] = "Technical context: \n\nCurrent architecture: \n\nConstraints: "
            template["problem_statement"] = "Technical problem to solve: "
            template["alternatives"] = [
                {
                    "name": "Option A",
                    "description": "Technical approach A",
                    "pros": [],
                    "cons": [],
                    "estimated_cost": None,
                    "estimated_benefit": None,
                    "estimated_risk": None
                },
                {
                    "name": "Option B",
                    "description": "Technical approach B",
                    "pros": [],
                    "cons": [],
                    "estimated_cost": None,
                    "estimated_benefit": None,
                    "estimated_risk": None
                }
            ]
            template["success_criteria"] = [
                "Performance requirements met",
                "Maintainable code",
                "Compatible with existing systems"
            ]
        
        elif template_type == "strategic":
            template["context"] = "Strategic context: \n\nMarket situation: \n\nCompetitive landscape: "
            template["problem_statement"] = "Strategic opportunity or challenge: "
            template["alternatives"] = [
                {
                    "name": "Strategy 1",
                    "description": "Strategic approach 1",
                    "pros": [],
                    "cons": [],
                    "estimated_cost": None,
                    "estimated_benefit": None,
                    "estimated_risk": None
                },
                {
                    "name": "Strategy 2",
                    "description": "Strategic approach 2",
                    "pros": [],
                    "cons": [],
                    "estimated_cost": None,
                    "estimated_benefit": None,
                    "estimated_risk": None
                }
            ]
            template["success_criteria"] = [
                "Alignment with company goals",
                "Market share impact",
                "Revenue potential"
            ]
        
        else:  # standard template
            template["alternatives"] = [
                {
                    "name": "Option 1",
                    "description": "",
                    "pros": [],
                    "cons": [],
                    "estimated_cost": None,
                    "estimated_benefit": None,
                    "estimated_risk": None
                },
                {
                    "name": "Option 2",
                    "description": "",
                    "pros": [],
                    "cons": [],
                    "estimated_cost": None,
                    "estimated_benefit": None,
                    "estimated_risk": None
                }
            ]
        
        return template
    
    def export_decision(self, decision_id: str, format: str = "text") -> str:
        """
        Export a decision in a specified format.
        
        Args:
            decision_id: ID of the decision
            format: Format to export in ("text", "markdown", "json")
            
        Returns:
            Exported decision as string
        """
        decision = self.get_decision(decision_id)
        if not decision:
            raise ValueError(f"Decision with ID {decision_id} not found")
        
        if format == "json":
            return decision.model_dump_json(indent=2)
        
        elif format == "markdown":
            # Create markdown representation
            md = []
            md.append(f"# {decision.title}")
            md.append("")
            md.append(f"**Decision Date:** {decision.decision_date.strftime('%Y-%m-%d')}")
            md.append(f"**Decision Maker:** {decision.decision_maker}")
            md.append(f"**Status:** {decision.status}")
            md.append("")
            md.append("## Description")
            md.append(decision.description)
            md.append("")
            md.append("## Context")
            md.append(decision.context)
            md.append("")
            md.append("## Problem Statement")
            md.append(decision.problem_statement)
            md.append("")
            md.append("## Alternatives Considered")
            
            for alt in decision.alternatives:
                is_chosen = str(alt.id) == decision.chosen_alternative
                chosen_marker = " ✓" if is_chosen else ""
                md.append(f"### {alt.name}{chosen_marker}")
                md.append(alt.description)
                md.append("")
                
                md.append("**Pros:**")
                for pro in alt.pros:
                    md.append(f"- {pro}")
                md.append("")
                
                md.append("**Cons:**")
                for con in alt.cons:
                    md.append(f"- {con}")
                md.append("")
                
                if alt.estimated_cost is not None:
                    md.append(f"**Estimated Cost:** {alt.estimated_cost}")
                if alt.estimated_benefit is not None:
                    md.append(f"**Estimated Benefit:** {alt.estimated_benefit}")
                if alt.estimated_risk is not None:
                    md.append(f"**Estimated Risk:** {alt.estimated_risk}")
                if alt.score is not None:
                    md.append(f"**Score:** {alt.score}")
                md.append("")
            
            md.append("## Decision Rationale")
            md.append(decision.rationale)
            md.append("")
            
            md.append("## Success Criteria")
            for criterion in decision.success_criteria:
                md.append(f"- {criterion}")
            md.append("")
            
            if decision.outcome_assessment:
                md.append("## Outcome Assessment")
                md.append(decision.outcome_assessment)
                md.append("")
            
            if decision.related_decisions:
                md.append("## Related Decisions")
                for related_id in decision.related_decisions:
                    related = self.get_decision(related_id)
                    if related:
                        md.append(f"- {related.title} ({related_id})")
                md.append("")
            
            return "\n".join(md)
        
        else:  # text format
            # Create plain text representation
            lines = []
            lines.append(f"DECISION: {decision.title}")
            lines.append(f"Date: {decision.decision_date.strftime('%Y-%m-%d')}")
            lines.append(f"Decision Maker: {decision.decision_maker}")
            lines.append(f"Status: {decision.status}")
            lines.append("")
            lines.append("DESCRIPTION")
            lines.append(decision.description)
            lines.append("")
            lines.append("CONTEXT")
            lines.append(decision.context)
            lines.append("")
            lines.append("PROBLEM STATEMENT")
            lines.append(decision.problem_statement)
            lines.append("")
            lines.append("ALTERNATIVES CONSIDERED")
            
            for alt in decision.alternatives:
                is_chosen = str(alt.id) == decision.chosen_alternative
                chosen_marker = " (CHOSEN)" if is_chosen else ""
                lines.append(f"{alt.name}{chosen_marker}")
                lines.append(alt.description)
                lines.append("")
                
                lines.append("Pros:")
                for pro in alt.pros:
                    lines.append(f"+ {pro}")
                lines.append("")
                
                lines.append("Cons:")
                for con in alt.cons:
                    lines.append(f"- {con}")
                lines.append("")
                
                if alt.estimated_cost is not None:
                    lines.append(f"Estimated Cost: {alt.estimated_cost}")
                if alt.estimated_benefit is not None:
                    lines.append(f"Estimated Benefit: {alt.estimated_benefit}")
                if alt.estimated_risk is not None:
                    lines.append(f"Estimated Risk: {alt.estimated_risk}")
                if alt.score is not None:
                    lines.append(f"Score: {alt.score}")
                lines.append("")
            
            lines.append("DECISION RATIONALE")
            lines.append(decision.rationale)
            lines.append("")
            
            lines.append("SUCCESS CRITERIA")
            for criterion in decision.success_criteria:
                lines.append(f"* {criterion}")
            lines.append("")
            
            if decision.outcome_assessment:
                lines.append("OUTCOME ASSESSMENT")
                lines.append(decision.outcome_assessment)
                lines.append("")
            
            if decision.related_decisions:
                lines.append("RELATED DECISIONS")
                for related_id in decision.related_decisions:
                    related = self.get_decision(related_id)
                    if related:
                        lines.append(f"* {related.title}")
                lines.append("")
            
            return "\n".join(lines)
    
    def calculate_decision_stats(self) -> Dict:
        """
        Calculate statistics about decisions in the registry.
        
        Returns:
            Dictionary with decision statistics
        """
        decisions = self.get_all_decisions()
        
        if not decisions:
            return {
                "total_decisions": 0,
                "status_counts": {},
                "alternatives_stats": {"avg": 0, "min": 0, "max": 0},
                "has_outcome_assessment": 0,
                "has_related_decisions": 0,
                "decision_makers": []
            }
        
        # Calculate status counts
        status_counts = {}
        for decision in decisions:
            if decision.status not in status_counts:
                status_counts[decision.status] = 0
            status_counts[decision.status] += 1
        
        # Calculate alternatives stats
        alt_counts = [len(d.alternatives) for d in decisions]
        avg_alternatives = sum(alt_counts) / len(alt_counts) if alt_counts else 0
        min_alternatives = min(alt_counts) if alt_counts else 0
        max_alternatives = max(alt_counts) if alt_counts else 0
        
        # Count decisions with outcome assessments
        outcome_count = sum(1 for d in decisions if d.outcome_assessment is not None)
        
        # Count decisions with related decisions
        related_count = sum(1 for d in decisions if d.related_decisions)
        
        # Count unique decision makers
        decision_makers = {}
        for decision in decisions:
            if decision.decision_maker not in decision_makers:
                decision_makers[decision.decision_maker] = 0
            decision_makers[decision.decision_maker] += 1
        
        return {
            "total_decisions": len(decisions),
            "status_counts": status_counts,
            "alternatives_stats": {
                "avg": avg_alternatives,
                "min": min_alternatives,
                "max": max_alternatives
            },
            "has_outcome_assessment": outcome_count,
            "has_related_decisions": related_count,
            "decision_makers": [
                {"name": name, "count": count}
                for name, count in sorted(decision_makers.items(), key=lambda x: x[1], reverse=True)
            ]
        }