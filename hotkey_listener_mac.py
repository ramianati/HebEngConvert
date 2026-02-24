"""
macOS-specific global hotkey listener using pynput.
Handles global keyboard shortcuts for clipboard monitoring.
"""
from pynput import keyboard
from threading import Thread
import logging

logger = logging.getLogger(__name__)


class HotkeyListenerMac:
    """macOS global hotkey listener using pynput."""
    
    def __init__(self, hotkey_combo, callback):
        """
        Initialize the hotkey listener.
        
        Args:
            hotkey_combo: Tuple of modifier keys and key, e.g., ('<cmd>', '<shift>', 'v')
            callback: Function to call when hotkey is pressed
        """
        self.hotkey_combo = hotkey_combo
        self.callback = callback
        self.listener = None
        self.current_keys = set()
        
        # Parse hotkey combo
        self.modifiers = set()
        self.trigger_key = None
        
        for key in hotkey_combo:
            key_str = key.lower().strip('<>')
            if key_str in ['cmd', 'command', 'ctrl', 'control', 'shift', 'alt', 'option']:
                self.modifiers.add(key_str)
            else:
                self.trigger_key = key_str
        
        logger.info(f"Initialized hotkey listener: modifiers={self.modifiers}, trigger={self.trigger_key}")
    
    def _normalize_key(self, key):
        """Normalize a key to a string representation."""
        if hasattr(key, 'char') and key.char:
            return key.char.lower()
        elif hasattr(key, 'name'):
            return key.name.lower()
        else:
            # Fallback for special keys: str(key) looks like "Key.cmd" or "'a'"
            return str(key).lower().strip("'").replace("key.", "")
    
    def _is_modifier_pressed(self, modifier):
        """Check if a specific modifier is currently pressed."""
        if modifier in ['cmd', 'command']:
            return keyboard.Key.cmd in self.current_keys or keyboard.Key.cmd_r in self.current_keys
        elif modifier in ['ctrl', 'control']:
            return keyboard.Key.ctrl in self.current_keys or keyboard.Key.ctrl_r in self.current_keys
        elif modifier == 'shift':
            return keyboard.Key.shift in self.current_keys or keyboard.Key.shift_r in self.current_keys
        elif modifier in ['alt', 'option']:
            return keyboard.Key.alt in self.current_keys or keyboard.Key.alt_r in self.current_keys
        return False
    
    def _check_hotkey(self):
        """Check if the current key combination matches the hotkey."""
        # Check all required modifiers are pressed
        for modifier in self.modifiers:
            if not self._is_modifier_pressed(modifier):
                return False
        
        # Check if trigger key is pressed
        if self.trigger_key:
            trigger_pressed = self.trigger_key in [self._normalize_key(k) for k in self.current_keys]
            return trigger_pressed
        
        return False
    
    def _on_press(self, key):
        """Handle key press events."""
        self.current_keys.add(key)
        
        if self._check_hotkey():
            logger.info(f"Hotkey triggered: {self.hotkey_combo}")
            try:
                self.callback()
            except Exception as e:
                logger.error(f"Error in hotkey callback: {e}")
    
    def _on_release(self, key):
        """Handle key release events."""
        if key in self.current_keys:
            self.current_keys.remove(key)
    
    def start(self):
        """Start listening for the hotkey."""
        if self.listener is None or not self.listener.running:
            try:
                self.listener = keyboard.Listener(
                    on_press=self._on_press,
                    on_release=self._on_release
                )
                self.listener.start()
                logger.info("Hotkey listener started")
            except Exception as e:
                # On macOS this can fail if Accessibility permissions are not granted.
                # The app should still launch — just without the global hotkey.
                logger.warning(
                    f"Could not start hotkey listener: {e}. "
                    "On macOS, grant Accessibility permission in "
                    "System Settings → Privacy & Security → Accessibility."
                )
    
    def stop(self):
        """Stop listening for the hotkey."""
        if self.listener and self.listener.running:
            self.listener.stop()
            self.current_keys.clear()
            logger.info("Hotkey listener stopped")
