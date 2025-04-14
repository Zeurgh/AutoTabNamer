# -*- coding: utf-8 -*-
import sublime
import sublime_plugin
import os

# --- Configuration Constants ---
# Prefix to find the name in the content (Note the space!)
HEADER_PREFIX = "## "
# Default name for unsaved tabs if no prefix is found
DEFAULT_UNSAVED_NAME = "! UnSaved"
# Maximum number of characters to read at the beginning to look for the ## prefix
# Avoids reading very large files just to check 2 lines.
LOOKAHEAD_LIMIT = 512 # Adjust if necessary
# Delay (in milliseconds) after the last modification before checking the ## name
DEBOUNCE_DELAY = 500 # 0.5 seconds

# --- Storage for Debouncing ---
# Dictionary to keep track of pending updates for each view
# Key: view.id(), Value: ID of the pending timeout
pending_updates = {}

# --- The EventListener Class ---

class AutoUnsavedTabNamerListener(sublime_plugin.EventListener):
    """
    Listens to Sublime Text events to automatically rename tabs
    of UNSAVED files according to the defined rules.
    """

    def _perform_rename(self, view):
        """
        Main function containing the checking and renaming logic.
        Called directly or via the debouncer.
        """
        # 1. Initial checks: Is the view valid? Is the file unsaved?
        if not view or not view.is_valid() or view.file_name() is not None:
            # If the view is invalid OR if the file HAS a name (is saved), stop here.
            return

        # 2. Determine the desired name
        desired_name = None

        # 2a. Look for the first line starting with HEADER_PREFIX
        content_start = view.substr(sublime.Region(0, min(view.size(), LOOKAHEAD_LIMIT)))
        lines = content_start.splitlines()

        for line in lines:
            cleaned_line = line.strip()
            if cleaned_line.startswith(HEADER_PREFIX):
                # First occurrence found!
                potential_name = cleaned_line[len(HEADER_PREFIX):].strip()
                if potential_name: # Ensure there is text after the prefix
                    desired_name = potential_name
                    break # Stop as soon as the first one is found

        # 2b. If no name was found via the prefix, use the default name
        if desired_name is None:
            desired_name = DEFAULT_UNSAVED_NAME

        # 3. Apply the name if different
        current_name = view.name()
        if current_name != desired_name:
            view.set_name(desired_name)
            # print("TabNamer: Set name to '{}'".format(desired_name)) # For debugging

    def _request_rename_debounced(self, view):
        """
        Requests a rename but uses debouncing to avoid excessive calls.
        Used primarily by on_modified_async.
        """
        if not view or not view.is_valid() or view.file_name() is not None:
            return # Do nothing for invalid views or saved files

        view_id = view.id()

        # Cancel any previous pending update for this view
        if view_id in pending_updates:
            sublime.cancel_timeout(pending_updates[view_id])
            # print("TabNamer: Debounce cancelled for view {}".format(view_id)) # Debug

        # Schedule the new update after the delay
        # Use set_timeout_async to avoid blocking the UI thread
        pending_updates[view_id] = sublime.set_timeout_async(
            lambda: self._run_debounced_action(view_id),
            DEBOUNCE_DELAY
        )
        # print("TabNamer: Debounce scheduled for view {}".format(view_id)) # Debug

    def _run_debounced_action(self, view_id):
        """
        Action executed after the debounce delay.
        Removes the task from the pending list and performs the rename.
        """
        # Check if the task is still relevant (just in case)
        if view_id in pending_updates:
            del pending_updates[view_id] # Remove from the pending tasks list

            # Find the view again using its ID (it might have been closed)
            view = self._find_view_by_id(view_id)
            if view:
                # print("TabNamer: Running debounced action for view {}".format(view_id)) # Debug
                self._perform_rename(view)
            # else:
                # print("TabNamer: View {} closed before debounced action.".format(view_id)) # Debug

    def _find_view_by_id(self, view_id):
        """ Searches for an active view across all windows by its ID. """
        for window in sublime.windows():
            for view in window.views():
                if view.id() == view_id:
                    return view
        return None

    # --- Event Handlers ---

    def on_new_async(self, view):
        """
        Called when a new (unsaved) tab is created.
        Immediately sets the default name.
        """
        # print("TabNamer: on_new_async") # Debug
        # No need for debounce here, we want the default name right away.
        # Use set_timeout for API safety.
        sublime.set_timeout(lambda: self._perform_rename(view), 0)

    def on_activated_async(self, view):
        """
        Called when a tab becomes active.
        Ensures the name is correct, especially for unsaved files.
        """
        # print("TabNamer: on_activated_async") # Debug
        # No need for debounce here. Quick check.
        sublime.set_timeout(lambda: self._perform_rename(view), 0)

    def on_modified_async(self, view):
        """
        Called when the content is modified.
        Triggers the check with debouncing.
        """
        # print("TabNamer: on_modified_async, requesting debounced rename") # Debug
        self._request_rename_debounced(view)

    # Note: on_load_async and on_post_save_async are not needed
    # as this plugin only targets unsaved files.