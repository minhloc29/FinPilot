"""
Evaluation script for testing agent responses
"""
from app.agents.planner_agent import PlannerAgent
import json
import asyncio
from typing import List, Dict
import sys
sys.path.append('../../backend')


class AgentEvaluator:
    """
    Evaluates agent responses against test queries
    """

    def __init__(self, test_queries_path: str):
        self.test_queries = self._load_test_queries(test_queries_path)
        self.planner = PlannerAgent()
        self.results = []

    def _load_test_queries(self, path: str) -> List[Dict]:
        """Load test queries from JSON file"""
        with open(path, 'r') as f:
            return json.load(f)

    async def evaluate_query(self, test_case: Dict) -> Dict:
        """Evaluate a single query"""
        query = test_case['query']
        expected_intent = test_case['expected_intent']
        expected_agents = test_case['expected_agents']

        print(f"\nEvaluating: {query}")

        # Get response from planner
        response = await self.planner.process(
            message=query,
            conversation_id=f"eval_{test_case['id']}"
        )

        # Extract actual agents used
        actual_agents = response.get('metadata', {}).get('agents_used', [])

        # Calculate metrics
        agent_match = set(expected_agents) == set(actual_agents)

        result = {
            'test_id': test_case['id'],
            'query': query,
            'expected_agents': expected_agents,
            'actual_agents': actual_agents,
            'agent_match': agent_match,
            'response_length': len(response.get('message', '')),
            'has_response': bool(response.get('message')),
            'tags': test_case.get('tags', [])
        }

        print(f"  Expected agents: {expected_agents}")
        print(f"  Actual agents: {actual_agents}")
        print(f"  Match: {agent_match}")

        return result

    async def run_evaluation(self):
        """Run evaluation on all test queries"""
        print("Starting evaluation...")

        for test_case in self.test_queries:
            result = await self.evaluate_query(test_case)
            self.results.append(result)

        # Calculate summary statistics
        self.print_summary()
        self.save_results()

    def print_summary(self):
        """Print evaluation summary"""
        total = len(self.results)
        agent_matches = sum(1 for r in self.results if r['agent_match'])
        has_response = sum(1 for r in self.results if r['has_response'])

        print("\n" + "="*50)
        print("EVALUATION SUMMARY")
        print("="*50)
        print(f"Total test cases: {total}")
        print(
            f"Agent routing accuracy: {agent_matches}/{total} ({agent_matches/total*100:.1f}%)")
        print(
            f"Response generation: {has_response}/{total} ({has_response/total*100:.1f}%)")

    def save_results(self, output_path: str = "evaluation_results.json"):
        """Save results to JSON file"""
        with open(output_path, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"\nResults saved to {output_path}")


if __name__ == "__main__":
    evaluator = AgentEvaluator("test_queries.json")
    asyncio.run(evaluator.run_evaluation())
