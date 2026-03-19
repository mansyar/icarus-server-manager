"""Module for querying Icarus Dedicated Server using the A2S protocol.
"""

import a2s
import datetime

class A2SClient:
    """Handles querying the game server for information like player count.
    """

    def get_player_count(self, host="127.0.0.1", port=27015):
        """Fetches the current player count from the server.

        Args:
            host (str): The server's IP address.
            port (int): The server's query port.

        Returns:
            int: Number of players currently connected, or 0 if query fails.
        """
        try:
            info = a2s.info((host, port), timeout=3.0)
            return info.player_count
        except Exception:
            # Gracefully handle timeouts or connection issues
            return 0

class A2SQueryService:
    """Service for fetching detailed server metrics and player lists.
    """
    
    def fetch_server_data(self, host="127.0.0.1", port=27015):
        """Fetches server info and player list.
        
        Args:
            host (str): The server's IP address.
            port (int): The server's query port.
            
        Returns:
            dict: Server metrics and player details.
        """
        try:
            # Info query
            info = a2s.info((host, port), timeout=3.0)
            
            # Players query
            players_list = a2s.players((host, port), timeout=3.0)
            
            players_data = []
            for p in players_list:
                players_data.append({
                    "name": p.name if p.name else "Unknown",
                    "playtime": self._format_duration(p.duration),
                    "score": p.score
                })
                
            return {
                "status": "Online",
                "server_name": info.server_name,
                "player_count": info.player_count,
                "players": players_data
            }
        except Exception:
            return {
                "status": "Offline",
                "player_count": 0,
                "players": []
            }
            
    def _format_duration(self, seconds):
        """Formats duration in seconds to HH:MM:SS.
        """
        if not seconds or seconds < 0:
            return "00:00:00"
        
        hours, remainder = divmod(int(seconds), 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"
