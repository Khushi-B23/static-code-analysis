"""A robust inventory management system"""

import json
import logging
from datetime import datetime

# Initialize logging before the class definition
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)


class Inventory:
    """Manages all inventory operations and state"""
    def __init__(self):
        self.stock_data = {}
        self.inventory_logs = []

    def add_item(self, item="default", qty=0):
        """
        Adds a quantity to the specified item and logs the transaction.
        Note: The 'logs' list is now managed internally as self.inventory_logs.
        """
        try:
            qty = int(qty)
        except (TypeError, ValueError):
            logging.warning("Invalid '%s': '%s'", item, qty)
            return

        if not isinstance(item, (str, int)) or not item:
            # E501 FIX: Broken into two lines
            logging.warning("Invalid or empty item identifier: '%s'. Skipping "
                            "addition.", item)
            return

        self.stock_data[item] = self.stock_data.get(item, 0) + qty
        self.inventory_logs.append(f"{datetime.now()}: Added {qty} of {item}")

    def remove_item(self, item, qty):
        """Removes a quantity from the specified item."""
        try:
            if item not in self.stock_data:
                raise KeyError(f"Item '{item}' not found in stock.")

            qty = int(qty)
            if qty < 0:
                raise ValueError("Removal quantity must be non-negative.")

            self.stock_data[item] -= qty

            if self.stock_data[item] <= 0:
                del self.stock_data[item]

        except (KeyError, ValueError) as e:
            logging.error("Error removing item: %s", e)

    def get_qty(self, item):
        """Returns the current stock quantity for an item."""
        return self.stock_data.get(item, 0)

    def load_data(self, file="inventory.json"):
        """Loads stock data from a JSON file."""
        try:
            with open(file, "r", encoding="utf-8") as file_handle:
                self.stock_data = json.loads(file_handle.read())
            logging.info("Successfully loaded inventory from %s.", file)
        except FileNotFoundError:
            logging.info("File '%s' not found", file)
        except json.JSONDecodeError:
            logging.error("Error decoding JSON from '%s'", file)
        except IOError as e:
            logging.error("An IO error occurred during file loading: %s", e)

    def save_data(self, file="inventory.json"):
        """Saves the current stock data to a JSON file."""
        try:
            with open(file, "w", encoding="utf-8") as file_handle:
                self.stock_data = json.loads(file_handle.read())
            logging.info("Successfully loaded inventory from %s.", file)
        except FileNotFoundError:
            logging.info("File '%s' not found.", file)
        except json.JSONDecodeError:
            logging.error("Error decoding JSON from '%s'", file)
        except IOError as e:
            logging.error("An IO error occurred during file loading: %s", e)

    def print_data(self):
        """Prints a report of all items and their quantities."""
        print("--- Items Report ---")
        for item, qty in self.stock_data.items():
            print(f"{item} -> {qty}")

    def check_low_items(self, threshold=5):
        """Checks for items whose quantity is below the specified threshold."""
        result = []
        for item, qty in self.stock_data.items():
            if qty < threshold:
                result.append(item)
        return result


def main():
    """Main function to demonstrate inventory operations and persistence."""
    inventory_manager = Inventory()
    inventory_manager.add_item("apple", 10)
    inventory_manager.add_item("banana", -2)
    inventory_manager.add_item(123, "ten")
    inventory_manager.remove_item("apple", 3)
    inventory_manager.remove_item("orange", 1)

    print("Apple stock:", inventory_manager.get_qty("apple"))
    print("Low items:", inventory_manager.check_low_items())

    inventory_manager.save_data()
    inventory_manager.load_data()
    inventory_manager.print_data()

    print("--- Transaction Logs ---")
    for log in inventory_manager.inventory_logs:
        print(log)


if __name__ == "__main__":
    main()
