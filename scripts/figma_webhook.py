"""
Figma Webhook Handler
Synchronisiert Prompts automatisch wenn Figma File sich ändert
"""

import json
import hmac
import hashlib
from typing import Dict, Optional
from datetime import datetime
from flask import Flask, request, jsonify
import os
import logging

logger = logging.getLogger(__name__)


class FigmaWebhookHandler:
    """Behandelt Figma Webhooks"""
    
    def __init__(self, webhook_secret: str):
        self.webhook_secret = webhook_secret
    
    def verify_signature(self, body: bytes, signature: str) -> bool:
        """Verifiziere Webhook Signature"""
        expected_sig = hmac.new(
            self.webhook_secret.encode(),
            body,
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(signature, expected_sig)
    
    def handle_file_update(self, data: Dict) -> Dict:
        """Handle Figma File Update Event"""
        event_type = data.get('event_type')
        file_id = data.get('file_id')
        
        logger.info(f"Handling event: {event_type} for file: {file_id}")
        
        if event_type == 'FILE_UPDATE':
            return self._handle_file_update(data)
        elif event_type == 'LIBRARY_PUBLISH':
            return self._handle_library_publish(data)
        else:
            return {"status": "unknown_event"}
    
    def _handle_file_update(self, data: Dict) -> Dict:
        """Handle FILE_UPDATE event"""
        file_id = data.get('file_id')
        timestamp = data.get('timestamp')
        
        changes = data.get('file_changes', [])
        
        logger.info(f"File {file_id} updated with {len(changes)} changes")
        
        # Trigger re-import
        return {
            "status": "file_updated",
            "file_id": file_id,
            "changes": len(changes),
            "timestamp": timestamp,
            "action": "trigger_import"
        }
    
    def _handle_library_publish(self, data: Dict) -> Dict:
        """Handle LIBRARY_PUBLISH event"""
        file_id = data.get('file_id')
        
        logger.info(f"Library published from file: {file_id}")
        
        return {
            "status": "library_published",
            "file_id": file_id,
            "action": "trigger_import"
        }


class FigmaWebhookServer:
    """Flask Server für Figma Webhooks"""
    
    def __init__(self, secret: str = None):
        self.app = Flask(__name__)
        self.secret = secret or os.getenv("FIGMA_WEBHOOK_SECRET")
        self.handler = FigmaWebhookHandler(self.secret)
        
        # Register routes
        self.app.add_url_rule('/webhook/figma', 'figma_webhook', 
                             self.handle_webhook, methods=['POST'])
        self.app.add_url_rule('/health', 'health', 
                             self.health_check, methods=['GET'])
    
    def handle_webhook(self):
        """Handle Figma webhook"""
        # Verifiziere Signature
        signature = request.headers.get('X-Figma-Signature', '')
        body = request.get_data()
        
        if not self.handler.verify_signature(body, signature):
            logger.warning("Invalid webhook signature")
            return jsonify({"error": "Invalid signature"}), 401
        
        try:
            data = json.loads(body)
            result = self.handler.handle_file_update(data)
            
            return jsonify(result), 200
        except Exception as e:
            logger.error(f"Error handling webhook: {e}")
            return jsonify({"error": str(e)}), 500
    
    def health_check(self):
        """Health check endpoint"""
        return jsonify({"status": "ok"}), 200
    
    def run(self, host: str = '0.0.0.0', port: int = 5000, debug: bool = False):
        """Start webhook server"""
        logger.info(f"Starting webhook server on {host}:{port}")
        self.app.run(host=host, port=port, debug=debug)


class FigmaWebhookClient:
    """Client zum Registrieren/Verwalten von Webhooks"""
    
    def __init__(self, api_token: str):
        self.api_token = api_token
        self.base_url = "https://api.figma.com/v1"
        self.headers = {
            "X-Figma-Token": api_token,
            "Content-Type": "application/json"
        }
    
    def register_webhook(self, team_id: str, callback_url: str, 
                        events: list = None) -> Dict:
        """Registriere Webhook"""
        import requests
        
        if not events:
            events = ["FILE_UPDATE", "LIBRARY_PUBLISH"]
        
        url = f"{self.base_url}/teams/{team_id}/webhooks"
        
        payload = {
            "event_types": events,
            "callback_url": callback_url,
            "description": "Auto-sync PROMPT frames"
        }
        
        logger.info(f"Registering webhook: {callback_url}")
        
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        
        return response.json()
    
    def list_webhooks(self, team_id: str) -> Dict:
        """Liste alle Webhooks auf"""
        import requests
        
        url = f"{self.base_url}/teams/{team_id}/webhooks"
        
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        
        return response.json()
    
    def delete_webhook(self, team_id: str, webhook_id: str) -> Dict:
        """Lösche Webhook"""
        import requests
        
        url = f"{self.base_url}/teams/{team_id}/webhooks/{webhook_id}"
        
        logger.info(f"Deleting webhook: {webhook_id}")
        
        response = requests.delete(url, headers=self.headers)
        response.raise_for_status()
        
        return {"status": "deleted"}


if __name__ == "__main__":
    # Start webhook server
    import sys
    
    secret = os.getenv("FIGMA_WEBHOOK_SECRET")
    if not secret:
        print("Error: FIGMA_WEBHOOK_SECRET environment variable required")
        sys.exit(1)
    
    port = int(os.getenv("PORT", 5000))
    
    server = FigmaWebhookServer(secret)
    server.run(port=port, debug=os.getenv("DEBUG", "False") == "True")
