"""Module for querying Icarus Dedicated Server using the A2S protocol.
"""

import a2s

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
