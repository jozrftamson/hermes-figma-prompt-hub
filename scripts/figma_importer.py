"""
Figma API Integration
Importiert PROMPT/* Frames direkt aus Figma
"""

import os
import json
import requests
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
from datetime import datetime
import logging

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class FigmaConfig:
    """Figma API Configuration"""
    api_token: str
    file_id: str
    base_url: str = "https://api.figma.com/v1"
    
    def __post_init__(self):
        if not self.api_token:
            raise ValueError("FIGMA_API_TOKEN environment variable or api_token parameter required")
        if not self.file_id:
            raise ValueError("FIGMA_FILE_ID environment variable or file_id parameter required")


@dataclass
class FigmaPromptMetadata:
    """Metadata extracted from Figma frame"""
    frame_id: str
    frame_name: str
    title: str = ""
    description: str = ""
    category: str = ""
    strategy: str = ""
    version: str = ""
    created_at: str = ""
    modified_at: str = ""
    figma_url: str = ""


class FigmaAPIClient:
    """Client für Figma API"""
    
    def __init__(self, config: FigmaConfig):
        self.config = config
        self.headers = {
            "X-Figma-Token": config.api_token,
            "Content-Type": "application/json"
        }
    
    def get_file(self) -> Dict:
        """Hole Figma File Metadaten"""
        url = f"{self.config.base_url}/files/{self.config.file_id}"
        
        logger.info(f"Fetching Figma file: {self.config.file_id}")
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        
        return response.json()
    
    def get_file_nodes(self, node_ids: List[str]) -> Dict:
        """Hole Nodes aus Figma File"""
        url = f"{self.config.base_url}/files/{self.config.file_id}/nodes"
        params = {"ids": ",".join(node_ids)}
        
        logger.info(f"Fetching {len(node_ids)} nodes from Figma")
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        
        return response.json()
    
    def get_text_content(self, node_id: str) -> str:
        """Hole Text-Inhalt aus Node"""
        url = f"{self.config.base_url}/files/{self.config.file_id}/nodes"
        params = {"ids": node_id}
        
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        return self._extract_text(data)
    
    def _extract_text(self, data: Dict) -> str:
        """Extrahiere Text aus Figma Node"""
        if 'nodes' not in data:
            return ""
        
        texts = []
        for node_id, node_data in data['nodes'].items():
            if 'document' in node_data:
                text = self._traverse_node(node_data['document'])
                texts.append(text)
        
        return "\n".join(texts).strip()
    
    def _traverse_node(self, node: Dict) -> str:
        """Traversiere Node-Tree und extrahiere Text"""
        texts = []
        
        if node.get('type') == 'TEXT':
            if 'characters' in node:
                texts.append(node['characters'])
        
        if 'children' in node:
            for child in node['children']:
                texts.append(self._traverse_node(child))
        
        return " ".join(texts)


class FigmaPromptExtractor:
    """Extrahiert Prompts aus Figma"""
    
    PROMPT_FRAME_PREFIX = "PROMPT/"
    
    def __init__(self, figma_client: FigmaAPIClient, file_key: str = ""):
        self.client = figma_client
        self.file_key = file_key or figma_client.config.file_id
        self.prompts: List[Dict] = []
    
    def extract_all_prompts(self) -> List[Dict]:
        """Extrahiere alle PROMPT/* Frames"""
        logger.info("Extracting all prompts from Figma...")
        
        # Hole Figma File
        file_data = self.client.get_file()
        
        # Finde alle PROMPT/* Frames
        prompt_frames = self._find_prompt_frames(file_data)
        
        logger.info(f"Found {len(prompt_frames)} prompt frames")
        
        # Extrahiere jeden Prompt
        for frame in prompt_frames:
            try:
                prompt = self._extract_prompt_from_frame(frame)
                self.prompts.append(prompt)
                logger.info(f"✅ Extracted: {prompt['name']}")
            except Exception as e:
                logger.error(f"❌ Failed to extract prompt from {frame.get('name')}: {e}")
        
        return self.prompts
    
    def _find_prompt_frames(self, file_data: Dict, parent_id: str = "") -> List[Dict]:
        """Finde alle PROMPT/* Frames rekursiv"""
        frames = []
        
        if 'document' not in file_data:
            return frames
        
        def traverse(node: Dict):
            name = node.get('name', '')
            
            # Prüfe ob Frame
            if node.get('type') in ['FRAME', 'COMPONENT']:
                # Prüfe ob PROMPT/* Frame
                if name.startswith(self.PROMPT_FRAME_PREFIX):
                    frames.append(node)
            
            # Rekursiv durch Kinder
            if 'children' in node:
                for child in node['children']:
                    traverse(child)
        
        traverse(file_data['document'])
        return frames
    
    def _extract_prompt_from_frame(self, frame: Dict) -> Dict:
        """Extrahiere Prompt aus einzelnem Frame"""
        frame_name = frame.get('name', '')
        frame_id = frame.get('id', '')
        
        logger.debug(f"Extracting frame: {frame_name}")
        
        # Parse Frame Name: PROMPT/id/version
        prompt_id, version = self._parse_frame_name(frame_name)
        
        # Hole Child-Frames
        children = self._get_frame_children(frame)
        
        # Extrahiere Metadaten
        metadata = self._extract_metadata(children.get('METADATA', {}))
        
        # Extrahiere Content
        content = self._extract_content(children.get('CONTENT', {}))
        
        # Extrahiere Beispiele
        examples = self._extract_examples(children.get('EXAMPLES', {}))
        
        # Extrahiere Strategy Config
        strategy_config = self._extract_strategy_config(children.get('STRATEGY_CONFIG', {}))
        
        prompt = {
            "prompt_id": prompt_id,
            "version": version or metadata.get('version', 'v1'),
            "name": metadata.get('title', prompt_id),
            "description": metadata.get('description', ''),
            "category": metadata.get('category', ''),
            "strategy": metadata.get('strategy', ''),
            "system": content.get('system', ''),
            "user_template": content.get('user_template', ''),
            "guardrails": content.get('guardrails', []),
            "output_format": content.get('output_format', ''),
            "examples": examples,
            "strategy_config": strategy_config,
            "figma_metadata": {
                "frame_id": frame_id,
                "frame_name": frame_name,
                "file_id": self.file_key,
                "figma_url": f"https://www.figma.com/file/{self.file_key}?node-id={frame_id}",
                "imported_at": datetime.now().isoformat()
            }
        }
        
        return prompt
    
    def _parse_frame_name(self, frame_name: str) -> Tuple[str, Optional[str]]:
        """Parse PROMPT/id/version format"""
        parts = frame_name.split('/')
        
        if len(parts) >= 3:
            prompt_id = parts[1]
            version = parts[2]
            return prompt_id, version
        elif len(parts) == 2:
            prompt_id = parts[1]
            return prompt_id, None
        else:
            raise ValueError(f"Invalid frame name format: {frame_name}")
    
    def _get_frame_children(self, frame: Dict) -> Dict[str, Dict]:
        """Hole Child-Frames nach Namen"""
        children = {}
        
        if 'children' not in frame:
            return children
        
        for child in frame['children']:
            name = child.get('name', '')
            if name in ['METADATA', 'CONTENT', 'EXAMPLES', 'STRATEGY_CONFIG']:
                children[name] = child
        
        return children
    
    def _extract_metadata(self, metadata_frame: Dict) -> Dict:
        """Extrahiere Metadata aus METADATA Frame"""
        metadata = {}
        
        if not metadata_frame or 'children' not in metadata_frame:
            return metadata
        
        for child in metadata_frame['children']:
            name = child.get('name', '')
            
            if child.get('type') == 'TEXT':
                text = self._extract_text_from_node(child)
                
                if name == 'title':
                    metadata['title'] = text
                elif name == 'description':
                    metadata['description'] = text
                elif name == 'category':
                    metadata['category'] = text
                elif name == 'strategy':
                    metadata['strategy'] = text
                elif name == 'version':
                    metadata['version'] = text
        
        return metadata
    
    def _extract_content(self, content_frame: Dict) -> Dict:
        """Extrahiere Content aus CONTENT Frame"""
        content = {
            'system': '',
            'user_template': '',
            'guardrails': [],
            'output_format': ''
        }
        
        if not content_frame or 'children' not in content_frame:
            return content
        
        for child in content_frame['children']:
            name = child.get('name', '')
            
            if child.get('type') == 'TEXT':
                text = self._extract_text_from_node(child)
                
                if name == 'system':
                    content['system'] = text
                elif name == 'user_template':
                    content['user_template'] = text
                elif name == 'guardrails':
                    # Parse guardrails (newline separated)
                    content['guardrails'] = [g.strip() for g in text.split('\n') if g.strip()]
                elif name == 'output_format':
                    content['output_format'] = text
        
        return content
    
    def _extract_examples(self, examples_frame: Dict) -> List[Dict]:
        """Extrahiere Examples aus EXAMPLES Frame"""
        examples = []
        
        if not examples_frame or 'children' not in examples_frame:
            return examples
        
        # Jedes Child-Frame ist ein Beispiel
        for child in examples_frame['children']:
            if child.get('type') in ['FRAME', 'GROUP']:
                example = self._extract_single_example(child)
                if example:
                    examples.append(example)
        
        return examples
    
    def _extract_single_example(self, example_frame: Dict) -> Optional[Dict]:
        """Extrahiere einzelnes Example"""
        example = {}
        
        if 'children' not in example_frame:
            return None
        
        for child in example_frame['children']:
            name = child.get('name', '')
            
            if child.get('type') == 'TEXT':
                text = self._extract_text_from_node(child)
                
                if name == 'input':
                    example['input'] = text
                elif name == 'output':
                    example['output'] = text
                elif name == 'explanation':
                    example['explanation'] = text
        
        if 'input' in example and 'output' in example:
            return example
        
        return None
    
    def _extract_strategy_config(self, strategy_frame: Dict) -> Dict:
        """Extrahiere Strategy Config"""
        config = {}
        
        if not strategy_frame or 'children' not in strategy_frame:
            return config
        
        for child in strategy_frame['children']:
            name = child.get('name', '')
            
            if child.get('type') == 'TEXT':
                text = self._extract_text_from_node(child)
                config[name] = text
        
        return config
    
    def _extract_text_from_node(self, node: Dict) -> str:
        """Extrahiere Text aus Text-Node"""
        if 'characters' in node:
            return node['characters']
        
        return ""


class FigmaPromptImporter:
    """Importiert Prompts aus Figma und speichert sie"""
    
    def __init__(self, config: FigmaConfig, output_dir: str = "./prompts"):
        self.config = config
        self.client = FigmaAPIClient(config)
        self.extractor = FigmaPromptExtractor(self.client, config.file_id)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def import_all(self) -> Dict:
        """Importiere alle Prompts aus Figma"""
        logger.info(f"Starting import from Figma file: {self.config.file_id}")
        
        # Extrahiere Prompts
        prompts = self.extractor.extract_all_prompts()
        
        if not prompts:
            logger.warning("No prompts found in Figma file")
            return {"imported": 0, "prompts": []}
        
        # Speichere jeden Prompt
        saved_files = []
        for prompt in prompts:
            file_path = self._save_prompt(prompt)
            saved_files.append(file_path)
            logger.info(f"Saved: {file_path}")
        
        # Erstelle Catalog
        catalog = self._create_catalog(prompts)
        catalog_path = self.output_dir / "catalog.json"
        with open(catalog_path, 'w', encoding='utf-8') as f:
            json.dump(catalog, f, indent=2)
        logger.info(f"Created catalog: {catalog_path}")
        
        return {
            "imported": len(prompts),
            "prompts": [p['name'] for p in prompts],
            "catalog": str(catalog_path),
            "output_dir": str(self.output_dir)
        }
    
    def _save_prompt(self, prompt: Dict) -> Path:
        """Speichere Prompt in JSON Datei"""
        filename = f"{prompt['prompt_id']}_v{prompt['version'].replace('.', '_')}.json"
        file_path = self.output_dir / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(prompt, f, indent=2)
        
        return file_path
    
    def _create_catalog(self, prompts: List[Dict]) -> Dict:
        """Erstelle Prompt Catalog"""
        return {
            "version": "1.0",
            "generated_at": datetime.now().isoformat(),
            "total_prompts": len(prompts),
            "prompts": [
                {
                    "id": p['prompt_id'],
                    "name": p['name'],
                    "description": p['description'],
                    "category": p['category'],
                    "strategy": p['strategy'],
                    "version": p['version'],
                    "file": f"{p['prompt_id']}_v{p['version'].replace('.', '_')}.json"
                }
                for p in prompts
            ]
        }


def import_from_figma(
    api_token: Optional[str] = None,
    file_id: Optional[str] = None,
    output_dir: str = "./prompts"
) -> Dict:
    """
    Hauptfunktion: Importiere Prompts aus Figma
    
    Args:
        api_token: Figma API Token (oder FIGMA_API_TOKEN env var)
        file_id: Figma File ID (oder FIGMA_FILE_ID env var)
        output_dir: Ausgabeverzeichnis
    
    Returns:
        Import-Ergebnis
    """
    api_token = api_token or os.getenv("FIGMA_API_TOKEN")
    file_id = file_id or os.getenv("FIGMA_FILE_ID")
    
    config = FigmaConfig(api_token=api_token, file_id=file_id)
    importer = FigmaPromptImporter(config, output_dir)
    
    return importer.import_all()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python figma_importer.py <api_token> <file_id> [output_dir]")
        print()
        print("Environment variables:")
        print("  FIGMA_API_TOKEN - Your Figma API token")
        print("  FIGMA_FILE_ID   - Your Figma file ID")
        print()
        sys.exit(1)
    
    api_token = sys.argv[1]
    file_id = sys.argv[2]
    output_dir = sys.argv[3] if len(sys.argv) > 3 else "./prompts"
    
    result = import_from_figma(api_token, file_id, output_dir)
    
    print()
    print("=" * 60)
    print("IMPORT COMPLETE")
    print("=" * 60)
    print(f"Imported: {result['imported']} prompts")
    print(f"Output: {result['output_dir']}")
    print()
    print("Prompts:")
    for prompt in result['prompts']:
        print(f"  - {prompt}")
