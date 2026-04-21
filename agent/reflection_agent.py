#!/usr/bin/env python3
"""
Daily Reflection Tree Agent
The agent loads a deterministic reflection tree and guides users through a conversation.
No LLM at runtime — fully deterministic based on structured data.
"""

import json
import os
from typing import Dict, List, Optional, Tuple
from pathlib import Path


class ReflectionTreeAgent:
    """Walks users through a deterministic reflection tree."""

    def __init__(self, tree_path: str):
        """Load the tree from JSON file."""
        with open(tree_path, 'r') as f:
            self.tree_data = json.load(f)
        
        self.nodes = {node['id']: node for node in self.tree_data['nodes']}
        self.current_node_id = 'START'
        self.state = {
            'answers': {},
            'signals': {'axis1': {}, 'axis2': {}, 'axis3': {}},
            'path': []
        }
        self.transcript = []

    def get_current_node(self) -> Dict:
        """Return the current node."""
        return self.nodes[self.current_node_id]

    def _interpolate_text(self, text: str) -> str:
        """Replace placeholders in text with actual answers."""
        if not text or text is None:
            return ""
        
        for node_id, answer in self.state['answers'].items():
            placeholder = f"{{{node_id}.answer}}"
            text = text.replace(placeholder, answer)
        
        return text

    def _route_decision(self, node: Dict) -> str:
        """
        Evaluate decision node routing.
        Format: "answer=Option1|Option2:TARGET;answer=Option3:TARGET2"
        """
        options_str = node['options']
        if not options_str:
            return None

        routes = options_str.split(';')
        last_answer_id = None
        
        # Find the most recent question node
        for visited_id in reversed(self.state['path']):
            if self.nodes[visited_id]['type'] == 'question':
                last_answer_id = visited_id
                break
        
        if not last_answer_id or last_answer_id not in self.state['answers']:
            return None
        
        user_answer = self.state['answers'][last_answer_id]

        for route in routes:
            if ':' not in route:
                continue
            
            condition, target = route.split(':')
            condition = condition.strip()
            target = target.strip()

            if condition.startswith('answer='):
                answers_str = condition[7:]  # Remove 'answer=' prefix
                possible_answers = [a.strip() for a in answers_str.split('|')]
                
                if user_answer in possible_answers:
                    return target
            
            elif condition.startswith('parentId='):
                parent_ids = [p.strip() for p in condition[9:].split('|')]
                if self.current_node_id in parent_ids:
                    return target

        return None

    def _accumulate_signals(self, node: Dict) -> None:
        """Tally signals from reflection nodes."""
        signal = node.get('signal')
        if not signal:
            return

        parts = signal.split(':')
        if len(parts) == 2:
            axis, pole = parts
            if axis not in self.state['signals']:
                self.state['signals'][axis] = {}
            if pole not in self.state['signals'][axis]:
                self.state['signals'][axis][pole] = 0
            self.state['signals'][axis][pole] += 1

    def _get_dominant_pole(self, axis: str) -> Tuple[str, str]:
        """
        Determine the dominant pole for an axis.
        Returns (pole_name, insight_text).
        """
        poles = self.state['signals'].get(axis, {})
        if not poles:
            return 'balanced', "There's nuance in how you showed up."

        max_pole = max(poles, key=poles.get)
        count = poles.get(max_pole, 0)

        insights = {
            'axis1': {
                'internal': 'You saw your hand in what happened. Agency.',
                'external': 'Circumstances pulled at you, but you still made calls.'
            },
            'axis2': {
                'contribution': 'You gave something today. That matters.',
                'entitlement': 'When you feel unseen, ask what you\'re trying to prove.'
            },
            'axis3': {
                'self_centric': 'Your world, clearly defined. Watch for isolation.',
                'altrocentric': 'You thought about others. That\'s where meaning lives.'
            }
        }

        insight = insights.get(axis, {}).get(max_pole, 'No dominant insight')
        return max_pole, insight

    def _generate_summary(self) -> str:
        """Generate the final summary with interpolated insights."""
        axis1_pole, axis1_insight = self._get_dominant_pole('axis1')
        axis2_pole, axis2_insight = self._get_dominant_pole('axis2')
        axis3_pole, axis3_insight = self._get_dominant_pole('axis3')

        summary_text = self.get_current_node()['text']
        summary_text = summary_text.replace('{axis1.dominant}', axis1_pole)
        summary_text = summary_text.replace('{axis1.insight}', axis1_insight)
        summary_text = summary_text.replace('{axis2.dominant}', axis2_pole)
        summary_text = summary_text.replace('{axis2.insight}', axis2_insight)
        summary_text = summary_text.replace('{axis3.dominant}', axis3_pole)
        summary_text = summary_text.replace('{axis3.insight}', axis3_insight)

        return summary_text

    def step(self, user_choice: Optional[int] = None) -> Tuple[str, Optional[List[str]], bool]:
        """
        Advance one step in the tree.
        
        Returns:
            (text_to_display, options_list, is_session_over)
        """
        node = self.get_current_node()
        self.state['path'].append(self.current_node_id)

        # Process node based on type
        if node['type'] == 'start':
            text = node['text']
            self.current_node_id = node['target'] or self._get_first_child()
            return text, None, False

        elif node['type'] == 'bridge':
            text = node['text']
            self.current_node_id = node['target'] or self._get_first_child()
            return text, None, False

        elif node['type'] == 'question':
            if user_choice is None:
                # First pass — present the question
                text = self._interpolate_text(node['text'])
                options = node['options']
                return text, options, False
            else:
                # User has chosen
                if 0 <= user_choice < len(node['options']):
                    chosen_option = node['options'][user_choice]
                    self.state['answers'][self.current_node_id] = chosen_option
                    self.transcript.append(f"Q: {self._interpolate_text(node['text'])}")
                    self.transcript.append(f"A: {chosen_option}")
                    
                    # Move to next node
                    next_node = self._get_next_node(node)
                    if next_node:
                        self.current_node_id = next_node
                    return None, None, False
                else:
                    return "Invalid choice.", node['options'], False

        elif node['type'] == 'decision':
            # Auto-advance with routing logic
            target = self._route_decision(node)
            if target and target in self.nodes:
                self.current_node_id = target
            else:
                self.current_node_id = self._get_first_child()
            return self.step()  # Recursively process next node

        elif node['type'] == 'reflection':
            text = self._interpolate_text(node['text'])
            self._accumulate_signals(node)
            self.transcript.append(f"Reflection: {text}")
            
            next_node = self._get_next_node(node)
            if next_node:
                self.current_node_id = next_node
            
            return text, None, False

        elif node['type'] == 'summary':
            text = self._generate_summary()
            self.transcript.append(f"Summary:\n{text}")
            
            next_node = self._get_next_node(node)
            if next_node:
                self.current_node_id = next_node
            
            return text, None, False

        elif node['type'] == 'end':
            self.transcript.append(f"End: {node['text']}")
            return node['text'], None, True

        return "Error: Unknown node type.", None, False

    def _get_first_child(self) -> Optional[str]:
        """Get the first child of current node."""
        for node in self.tree_data['nodes']:
            if node.get('parentId') == self.current_node_id:
                return node['id']
        return None

    def _get_next_node(self, current_node: Dict) -> Optional[str]:
        """Get the next node after current."""
        if current_node.get('target'):
            return current_node['target']
        
        # Default: find first child
        return self._get_first_child()

    def get_transcript(self) -> str:
        """Get the full transcript of the session."""
        return '\n'.join(self.transcript)


class InteractiveSession:
    """Run an interactive CLI session."""

    def __init__(self, tree_path: str):
        self.agent = ReflectionTreeAgent(tree_path)

    def run(self) -> None:
        """Interactive loop."""
        print("\n" + "=" * 60)
        print("Daily Reflection Tree")
        print("=" * 60 + "\n")

        is_done = False
        
        while not is_done:
            node = self.agent.get_current_node()
            
            # First presentation of question/text
            text, options, is_done = self.agent.step()
            
            if text:
                print(f"\n{text}")
            
            if is_done:
                print("\n" + "=" * 60)
                print("Session Complete")
                print("=" * 60)
                break
            
            if options:
                # Question node — wait for user input
                for i, option in enumerate(options, 1):
                    print(f"  {i}. {option}")
                
                while True:
                    try:
                        choice = int(input("\nYour choice (number): "))
                        if 0 <= choice - 1 < len(options):
                            _, _, is_done = self.agent.step(choice - 1)
                            if is_done:
                                print("\n" + "=" * 60)
                                print("Session Complete")
                                print("=" * 60)
                            break
                        else:
                            print("Invalid choice. Try again.")
                    except ValueError:
                        print("Please enter a number.")
            else:
                # Non-interactive node (bridge, reflection, etc.) — just continue
                input("\nPress Enter to continue...")

        # Save transcript
        transcript_text = self.agent.get_transcript()
        print("\n" + "=" * 60)
        print("Your Reflection Session")
        print("=" * 60)
        print(transcript_text)
        
        # Optionally save to file
        transcript_file = Path('transcripts') / f'session_{self._get_timestamp()}.txt'
        transcript_file.parent.mkdir(exist_ok=True)
        with open(transcript_file, 'w') as f:
            f.write(transcript_text)
        print(f"\n[Transcript saved to {transcript_file}]")

    def _get_timestamp(self) -> str:
        """Generate a timestamp for file naming."""
        from datetime import datetime
        return datetime.now().strftime('%Y%m%d_%H%M%S')


if __name__ == '__main__':
    tree_path = os.path.join(os.path.dirname(__file__), '..', 'tree', 'reflection-tree.json')
    
    if not os.path.exists(tree_path):
        print(f"Tree file not found at {tree_path}")
        exit(1)
    
    session = InteractiveSession(tree_path)
    session.run()
