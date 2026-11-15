
# MINT v0.8 - Savings Goals

import json
import os
from datetime import datetime

from kivy.app import App
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle, Rectangle

from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView


Window.clearcolor = (0.055, 0.065, 0.07, 1)

INCOME_CATEGORIES = [
    "Salary", "Side job", "Gifts", "Other"
]

EXPENSE_CATEGORIES = [
    "Food", "Transport", "Housing",
    "Shopping", "Entertainment", "Health", "Other"
]


# -------------------------
# PROGRESS BAR
# -------------------------

class MintProgressBar(Widget):

    def __init__(self, percentage=0, **kwargs):
        super().__init__(**kwargs)

        self.percentage = percentage

        with self.canvas:
            Color(0.16, 0.20, 0.20, 1)

            self.background = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(5)]
            )

            Color(0.25, 0.78, 0.57, 1)

            self.foreground = RoundedRectangle(
                pos=self.pos,
                size=(0, self.height),
                radius=[dp(5)]
            )

        self.bind(
            pos=self.update_canvas,
            size=self.update_canvas
        )

    def update_canvas(self, *args):

        self.background.pos = self.pos
        self.background.size = self.size

        fill_width = self.width * self.percentage / 100

        self.foreground.pos = self.pos
        self.foreground.size = (
            fill_width,
            self.height
        )


# -------------------------
# -------------------------
# MINT CHART
# -------------------------

class MintChartBar(Widget):

    def __init__(self, percentage=0, bar_color=(0.3, 0.9, 0.6, 1), **kwargs):
        super().__init__(**kwargs)

        self.percentage = percentage
        self.bar_color = bar_color

        with self.canvas:
            Color(0.16, 0.20, 0.20, 1)

            self.bg = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(5)]
            )

            Color(*self.bar_color)

            self.fill = RoundedRectangle(
                pos=self.pos,
                size=(0, self.height),
                radius=[dp(5)]
            )

        self.bind(
            pos=self.update_bar,
            size=self.update_bar
        )

    def update_bar(self, *args):

        self.bg.pos = self.pos
        self.bg.size = self.size

        width = self.width * self.percentage / 100

        self.fill.pos = self.pos
        self.fill.size = (width, self.height)


class MintChart(BoxLayout):

    def __init__(self, income=0, expenses=0, **kwargs):

        super().__init__(
            orientation="vertical",
            spacing=dp(10),
            padding=dp(12),
            size_hint_y=None,
            height=dp(95),
            **kwargs
        )

        maximum = max(income, expenses, 1)

        income_percent = income / maximum * 100
        expense_percent = expenses / maximum * 100

        self.add_widget(
            Label(
                text="MONTHLY OVERVIEW",
                font_size=11,
                bold=True,
                color=(0.7, 0.75, 0.73, 1),
                size_hint_y=None,
                height=dp(20)
            )
        )

        for name, amount, percent, color in [
            ("INCOME", income, income_percent, (0.3, 0.9, 0.6, 1)),
            ("EXPENSES", expenses, expense_percent, (1, 0.35, 0.35, 1))
        ]:

            row = BoxLayout(
                orientation="horizontal",
                spacing=dp(8)
            )

            row.add_widget(
                Label(
                    text=name,
                    font_size=10,
                    color=(0.7, 0.75, 0.73, 1),
                    size_hint_x=0.3
                )
            )

            row.add_widget(
                MintChartBar(
                    percentage=percent,
                    bar_color=color
                )
            )

            self.add_widget(row)# MAIN APP
# -------------------------

class MintApp(App):

    def build(self):

        self.title = "MINT"
        self.load_data()

        self.current_screen = "home"

        self.root = BoxLayout(
            orientation="vertical",
            padding=dp(15),
            spacing=dp(10)
        )

        title = Label(
            text="MINT",
            font_size=30,
            bold=True,
            color=(0.35, 0.85, 0.65, 1),
            size_hint_y=None,
            height=dp(45)
        )

        self.root.add_widget(title)

        self.content = BoxLayout(
            orientation="vertical"
        )

        self.root.add_widget(self.content)

        # Navigation

        # Navigation

        navigation = BoxLayout(
            spacing=dp(5),
            size_hint_y=None,
            height=dp(50)
        )

        self.home_button = Button(
            text="HOME",
            background_normal="",
            background_color=(0.2, 0.65, 0.45, 1)
        )

        self.stats_button = Button(
            text="STATS",
            background_normal="",
            background_color=(0.2, 0.25, 0.25, 1)
        )

        self.goals_button = Button(
            text="GOALS",
            background_normal="",
            background_color=(0.2, 0.25, 0.25, 1)
        )
     
        self.settings_button = Button(
            text="SETTINGS",
            background_normal="",
            background_color=(0.2, 0.25, 0.25, 1)
        )
        self.home_button.bind(
            on_release=lambda x: self.show_home()
        )

        self.stats_button.bind(
            on_release=lambda x: self.show_statistics()
        )

        self.goals_button.bind(
            on_release=lambda x: self.show_goals()
        )
        self.settings_button.bind(
            on_release=lambda x: self.show_settings()
        )
        navigation.add_widget(self.home_button)
        navigation.add_widget(self.stats_button)
        navigation.add_widget(self.goals_button)
        navigation.add_widget(self.settings_button)
        self.root.add_widget(navigation)

        self.show_home()

        return self.root

    def update_navigation(self):

        active_color = (0.2, 0.65, 0.45, 1)
        inactive_color = (0.2, 0.25, 0.25, 1)

        self.home_button.background_color = (
            active_color if self.current_screen == "home"
            else inactive_color
        )

        self.stats_button.background_color = (
            active_color if self.current_screen == "statistics"
            else inactive_color
        )

        self.goals_button.background_color = (
            active_color if self.current_screen == "goals"
            else inactive_color
        )
        self.settings_button.background_color = (
            active_color if self.current_screen == "settings"
            else inactive_color
        )
    # -------------------------
    # CURRENCY
    # -------------------------

    def get_currency_symbol(self):

        symbols = {
            "KZT": "KZT",
            "USD": "USD",
            "EUR": "EUR"
        }

        return symbols.get(self.currency, "KZT")
    # -------------------------
    # DATA
    # -------------------------

    def load_data(self):

        path = os.path.join(
            self.user_data_dir,
            "mint_data.json"
        )

        try:
            with open(path, "r", encoding="utf-8") as file:
                data = json.load(file)

            self.balance = float(data["balance"])
            self.transactions = []

            for item in data["transactions"]:

                if isinstance(item, dict):
                    self.transactions.append(item)

                else:
                    sign, amount, kind = item

                    self.transactions.append({
                        "sign": sign,
                        "amount": float(amount),
                        "kind": kind,
                        "category": "Other",
                        "date": "Unknown"
                    })

            # Load savings goals
            self.goals = data.get("goals", [])
                        # Load spending limits
            self.limits = data.get("limits", {})
                        # Load currency
            self.currency = data.get("currency", "KZT")

        except (
            FileNotFoundError,
            KeyError,
            ValueError,
            TypeError,
            json.JSONDecodeError
        ):
            self.balance = 0.0
            self.transactions = []
            self.goals = []
            self.limits = {}
            self.currency = "KZT"

    def save_data(self):

        path = os.path.join(
            self.user_data_dir,
            "mint_data.json"
        )

        data = {
            "balance": self.balance,
            "transactions": self.transactions,
            "goals": self.goals,
            "limits": self.limits,
            "currency": self.currency
        }
        with open(path, "w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False
            )

    # -------------------------
    # HOME SCREEN
    # -------------------------
    def get_month_totals(self):

        current_month = datetime.now().strftime("%m.%Y")

        income = 0
        expenses = 0

        for item in self.transactions:

            date = item.get("date", "")

            if current_month not in date:
                continue

            amount = float(item.get("amount", 0))
            kind = item.get("kind", "")

            if kind == "income":
                income += amount

            elif kind == "expense":
                expenses += amount

        return income, expenses
    def show_home(self):

        self.current_screen = "home"
        self.update_navigation()
        self.content.clear_widgets()

        screen = BoxLayout(
            orientation="vertical",
            spacing=dp(8),
            padding=[dp(16), dp(18), dp(16), dp(10)]
        )

        # HEADER

        header = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(40)
        )

        header.add_widget(
            Label(
                text="MINT",
                font_size=25,
                bold=True,
                color=(0.35, 0.85, 0.65, 1),
                halign="left"
            )
        )

        header.add_widget(
            Label(
                text="PERSONAL FINANCE",
                font_size=10,
                color=(0.55, 0.6, 0.6, 1),
                halign="right"
            )
        )

        screen.add_widget(header)

        # BALANCE CARD

        balance_card = BoxLayout(
            orientation="vertical",
            padding=dp(18),
            spacing=dp(10),
            size_hint_y=None,
            height=dp(125)
        )

        with balance_card.canvas.before:
            Color(0.10, 0.13, 0.12, 1)

            balance_card.bg = RoundedRectangle(
                pos=balance_card.pos,
                size=balance_card.size,
                radius=[dp(18)]
            )

        balance_card.bind(
            pos=lambda instance, value:
            setattr(instance.bg, "pos", value),
            size=lambda instance, value:
            setattr(instance.bg, "size", value)
        )

        balance_card.add_widget(
            Label(
                text="TOTAL BALANCE",
                font_size=12,
                color=(0.6, 0.7, 0.65, 1),
                halign="left",
                size_hint_y=None,
                height=dp(25)
            )
        )

        self.balance_label = Label(
            text=f"{self.balance:,.2f} {self.get_currency_symbol()}",
            font_size=29,
            bold=True,
            color=(0.35, 0.9, 0.68, 1),
            halign="left"
        )

        balance_card.add_widget(self.balance_label)

        balance_card.add_widget(
            Label(
                text="Your money at a glance",
                font_size=11,
                color=(0.5, 0.58, 0.54, 1),
                halign="left"
            )
        )

        screen.add_widget(balance_card)
                # MONTHLY INCOME AND EXPENSES

        monthly_income, monthly_expenses = self.get_month_totals()

        monthly_cards = BoxLayout(
            orientation="horizontal",
            spacing=dp(12),
            size_hint_y=None,
            height=dp(85)
        )

        income_card = BoxLayout(
            orientation="vertical",
            padding=dp(12),
            spacing=dp(5)
        )

        with income_card.canvas.before:
            Color(0.09, 0.17, 0.13, 1)
            income_card.bg = RoundedRectangle(
                pos=income_card.pos,
                size=income_card.size,
                radius=[dp(14)]
            )

        income_card.bind(
            pos=lambda instance, value:
            setattr(instance.bg, "pos", value),
            size=lambda instance, value:
            setattr(instance.bg, "size", value)
        )

        income_card.add_widget(
            Label(
                text="INCOME THIS MONTH",
                font_size=10,
                color=(0.6, 0.75, 0.65, 1)
            )
        )

        income_card.add_widget(
            Label(
                text=f"+{monthly_income:,.0f} {self.get_currency_symbol()}",
                font_size=19,
                bold=True,
                color=(0.35, 0.9, 0.65, 1)
            )
        )

        expense_card = BoxLayout(
            orientation="vertical",
            padding=dp(12),
            spacing=dp(5)
        )

        with expense_card.canvas.before:
            Color(0.18, 0.10, 0.10, 1)
            expense_card.bg = RoundedRectangle(
                pos=expense_card.pos,
                size=expense_card.size,
                radius=[dp(14)]
            )

        expense_card.bind(
            pos=lambda instance, value:
            setattr(instance.bg, "pos", value),
            size=lambda instance, value:
            setattr(instance.bg, "size", value)
        )

        expense_card.add_widget(
            Label(
                text="EXPENSES THIS MONTH",
                font_size=10,
                color=(0.75, 0.6, 0.6, 1)
            )
        )

        expense_card.add_widget(
            Label(
                
                text=f"-{monthly_expenses:,.0f} {self.get_currency_symbol()}",
                font_size=19,
                bold=True,
                color=(1, 0.4, 0.4, 1)
            )
        )

        monthly_cards.add_widget(income_card)
        monthly_cards.add_widget(expense_card)
        screen.add_widget(monthly_cards)

        # MONTHLY CHART

        chart = MintChart(
            income=monthly_income,
            expenses=monthly_expenses
        )

        screen.add_widget(chart)

        # ACTION BUTTONS

        actions = BoxLayout(
            orientation="horizontal",
            spacing=dp(12),
            size_hint_y=None,
            height=dp(55)
        )

        income_button = Button(
            text="+ INCOME",
            background_normal="",
            background_color=(0.2, 0.65, 0.45, 1),
            font_size=14,
            bold=True
        )

        expense_button = Button(
            text="- EXPENSE",
            background_normal="",
            background_color=(0.20, 0.23, 0.23, 1),
            font_size=14,
            bold=True
        )

        income_button.bind(
            on_release=lambda x:
            self.open_transaction("income")
        )

        expense_button.bind(
            on_release=lambda x:
            self.open_transaction("expense")
        )

        actions.add_widget(income_button)
        actions.add_widget(expense_button)

        screen.add_widget(actions)

        # HISTORY HEADER

        history_header = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(35)
        )

        history_header.add_widget(
            Label(
                text="RECENT ACTIVITY",
                font_size=14,
                bold=True,
                color=(0.9, 0.93, 0.92, 1),
                halign="left"
            )
        )

        screen.add_widget(history_header)

        # TRANSACTION LIST

        scroll = ScrollView(
            do_scroll_x=False
        )

        self.history_box = BoxLayout(
            orientation="vertical",
            spacing=dp(8),
            size_hint_y=None
        )

        self.history_box.bind(
            minimum_height=self.history_box.setter("height")
        )

        scroll.add_widget(self.history_box)

        screen.add_widget(scroll)

        self.content.add_widget(screen)

        self.update_history()
            # -------------------------
    # TRANSACTION HISTORY
    # -------------------------

    def update_history(self):

        self.history_box.clear_widgets()

        if not self.transactions:
            self.history_box.add_widget(
                Label(
                    text="No transactions yet",
                    color=(0.5, 0.55, 0.55, 1),
                    size_hint_y=None,
                    height=dp(50)
                )
            )
            return

        for index in range(len(self.transactions) - 1, -1, -1):

            item = self.transactions[index]

            sign = item.get("sign", "")
            amount = float(item.get("amount", 0))
            category = item.get("category", "Other")
            date = item.get("date", "")
            description = item.get("description", "")

            color = (
                (0.35, 0.85, 0.65, 1)
                if sign == "+"
                else (1, 0.4, 0.4, 1)
            )

            row = BoxLayout(
                orientation="horizontal",
                spacing=dp(5),
                size_hint_y=None,
                height=dp(65)
            )

            info = BoxLayout(
                orientation="vertical",
                spacing=dp(2)
            )

            category_label = Label(
                text=category,
                font_size=13,
                bold=True,
                color=(0.9, 0.94, 0.92, 1),
                halign="left",
                valign="bottom"
            )
            description_label = Label(
                text=description,
                font_size=11,
                color=(0.65, 0.72, 0.69, 1),
                halign="left",
                valign="middle"
            )

            date_label = Label(
                text=date,
                font_size=10,
                color=(0.5, 0.58, 0.55, 1),
                halign="left",
                valign="top"
            )

            for label in (category_label, description_label, date_label):
                label.bind(
                    size=lambda instance, value:
                    setattr(instance, "text_size", value)
                )

            info.add_widget(category_label)
            info.add_widget(description_label)
            info.add_widget(date_label)

            value = Label(
                text=f"{sign}{amount:,.2f}",
                color=color,
                size_hint_x=0.8
            )
            edit_button = Button(
                text="EDIT",
                size_hint=(None, None),
                size=(dp(45), dp(30)),
font_size=10,
                background_normal="",
                background_color=(0.15, 0.4, 0.3, 1)
            )

            edit_button.bind(
                on_release=lambda button, i=index:
                self.edit_transaction(i)
            )

            delete_button = Button(
                text="DELETE",
                size_hint=(None, None),
                size=(dp(45), dp(30)),
font_size=10,
                bold=True,
                background_normal="",
                background_color=(0.35, 0.16, 0.18, 1)
            )

            delete_button.bind(
                on_release=lambda button, i=index:
                self.confirm_delete_transaction(i)
            )

            row.add_widget(info)
            row.add_widget(value)
            row.add_widget(edit_button)
            row.add_widget(delete_button)    
            
            self.history_box.add_widget(row)
            separator = Widget(
                size_hint_y=None,
                height=dp(1)
            )

            with separator.canvas:
                Color(0.22, 0.29, 0.27, 1)
                separator.rect = Rectangle(
                    pos=separator.pos,
                    size=separator.size
                )

            separator.bind(
                pos=lambda instance, value:
                setattr(instance.rect, "pos", value),
                size=lambda instance, value:
                setattr(instance.rect, "size", value)
            )

            self.history_box.add_widget(separator)

    # -------------------------
    # ADD INCOME / EXPENSE
    # -------------------------

    def open_transaction(self, transaction_type):

        categories = (
            INCOME_CATEGORIES
            if transaction_type == "income"
            else EXPENSE_CATEGORIES
        )

        content = BoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=dp(12)
        )

        amount_input = TextInput(
            hint_text=f"Amount in {self.get_currency_symbol()}",
            multiline=False,
            input_filter="float",
            size_hint_y=None,
            height=dp(48)
        )

        category_spinner = Spinner(
            text=categories[0],
            values=categories,
            size_hint_y=None,
            height=dp(48)
        )
        description_input = TextInput(
            hint_text="Description (optional)",
            multiline=False,
            size_hint_y=None,
            height=dp(48)
        )

        status = Label(
            text="",
            color=(1, 0.4, 0.4, 1)
        )

        save_button = Button(
            text="SAVE",
            size_hint_y=None,
            height=dp(48),
            background_normal="",
            background_color=(0.2, 0.65, 0.45, 1)
        )

        content.add_widget(amount_input)
        content.add_widget(description_input)
        content.add_widget(category_spinner)
        content.add_widget(status)
        content.add_widget(save_button)

        popup = Popup(
            title=(
                "Add income"
                if transaction_type == "income"
                else "Add expense"
            ),
            content=content,
            size_hint=(0.88, 0.55)
        )

        def save_transaction(*args):

            try:
                amount = float(
                    amount_input.text.replace(",", ".")
                )

                if amount <= 0:
                    status.text = "Enter a positive amount"
                    return

                sign = (
                    "+"
                    if transaction_type == "income"
                    else "-"
                )

                self.transactions.append({
                    "sign": sign,
                    "amount": amount,
                    "kind": transaction_type,
                    "category": category_spinner.text,
                    "description": description_input.text.strip(),
                    "date": datetime.now().strftime(
                        "%d.%m.%Y %H:%M"
                    )
                })

                if transaction_type == "income":
                    self.balance += amount
                else:
                    self.balance -= amount

                self.save_data()
                popup.dismiss()
                self.show_home()

            except ValueError:
                status.text = "Enter a valid amount"

        save_button.bind(on_release=save_transaction)

        popup.open()
            # -------------------------
    # EDIT TRANSACTION
    # -------------------------

    def edit_transaction(self, index):

        if index >= len(self.transactions):
            return

        item = self.transactions[index]

        transaction_type = item.get("kind", "")

        if not transaction_type:
            transaction_type = (
                "income"
                if item.get("sign") == "+"
                else "expense"
            )

        categories = (
            INCOME_CATEGORIES
            if transaction_type == "income"
            else EXPENSE_CATEGORIES
        )

        content = BoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=dp(12)
        )

        amount_input = TextInput(
            text=str(item.get("amount", 0)),
            hint_text="Amount",
            multiline=False,
            input_filter="float",
            size_hint_y=None,
            height=dp(48)
        )

        category_spinner = Spinner(
            text=item.get("category", categories[0]),
            values=categories,
            size_hint_y=None,
            height=dp(48)
        )
        description_input = TextInput(
            text=item.get("description", ""),
            hint_text="Description (optional)",
            multiline=False,
            size_hint_y=None,
            height=dp(48)
        )

        type_spinner = Spinner(
            text=transaction_type.upper(),
            values=("INCOME", "EXPENSE"),
            size_hint_y=None,
            height=dp(48)
        )

        status = Label(
            text="",
            color=(1, 0.4, 0.4, 1)
        )

        save_button = Button(
            text="SAVE CHANGES",
            size_hint_y=None,
            height=dp(48),
            background_normal="",
            background_color=(0.2, 0.65, 0.45, 1)
        )

        content.add_widget(amount_input)
        content.add_widget(type_spinner)
        content.add_widget(category_spinner)
        content.add_widget(description_input)
        content.add_widget(status)
        content.add_widget(save_button)

        popup = Popup(
            title="Edit transaction",
            content=content,
            size_hint=(0.88, 0.65)
        )

        def save_changes(*args):

            try:
                new_amount = float(
                    amount_input.text.replace(",", ".")
                )

                if new_amount <= 0:
                    status.text = "Enter a positive amount"
                    return

                old_amount = float(item.get("amount", 0))
                old_kind = item.get("kind", transaction_type)

                if not old_kind:
                    old_kind = (
                        "income"
                        if item.get("sign") == "+"
                        else "expense"
                    )

                new_kind = type_spinner.text.lower()

                # Restore old balance
                if old_kind == "income":
                    self.balance -= old_amount
                else:
                    self.balance += old_amount

                # Apply new transaction
                if new_kind == "income":
                    self.balance += new_amount
                    sign = "+"
                else:
                    self.balance -= new_amount
                    sign = "-"

                item["amount"] = new_amount
                item["kind"] = new_kind
                item["sign"] = sign
                item["category"] = category_spinner.text
                item["description"] = description_input.text.strip()

                self.save_data()
                popup.dismiss()
                self.show_home()

            except ValueError:
                status.text = "Enter a valid amount"

        save_button.bind(on_release=save_changes)

        popup.open()

    # -------------------------
    # DELETE TRANSACTION
    # -------------------------

    def confirm_delete_transaction(self, index):

        content = BoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=dp(12)
        )

        content.add_widget(
            Label(text="Delete this transaction?")
        )

        buttons = BoxLayout(
            spacing=dp(10),
            size_hint_y=None,
            height=dp(45)
        )

        cancel_button = Button(text="CANCEL")
        delete_button = Button(
            text="DELETE",
            background_normal="",
            background_color=(0.55, 0.2, 0.2, 1)
        )

        buttons.add_widget(cancel_button)
        buttons.add_widget(delete_button)
        content.add_widget(buttons)

        popup = Popup(
            title="Confirm deletion",
            content=content,
            size_hint=(0.85, 0.3)
        )

        def delete_transaction(*args):

            if index >= len(self.transactions):
                popup.dismiss()
                return

            item = self.transactions.pop(index)

            amount = float(item.get("amount", 0))
            kind = item.get("kind", "")

            if kind == "income" or item.get("sign") == "+":
                self.balance -= amount
            else:
                self.balance += amount

            self.save_data()
            popup.dismiss()
            self.show_home()

        cancel_button.bind(
            on_release=lambda button: popup.dismiss()
        )

        delete_button.bind(
            on_release=delete_transaction
        )

        popup.open()

    # -------------------------
    # ADD MONEY TO GOAL
    # -------------------------

    def open_add_money(self, index):

        content = BoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=dp(12)
        )

        amount_input = TextInput(
            hint_text=f"Amount in {self.get_currency_symbol()}",
            multiline=False,
            input_filter="float",
            size_hint_y=None,
            height=dp(48)
        )

        status = Label(
            text="",
            color=(1, 0.4, 0.4, 1)
        )

        add_button = Button(
            text="ADD MONEY",
            size_hint_y=None,
            height=dp(48),
            background_normal="",
            background_color=(0.2, 0.65, 0.45, 1)
        )

        content.add_widget(amount_input)
        content.add_widget(status)
        content.add_widget(add_button)

        popup = Popup(
            title="Add money to goal",
            content=content,
            size_hint=(0.88, 0.4)
        )

        def add_money(*args):

            try:
                amount = float(
                    amount_input.text.replace(",", ".")
                )

                if amount <= 0:
                    status.text = "Enter a positive amount"
                    return

                self.goals[index]["saved"] = (
                    float(self.goals[index]["saved"]) + amount
                )

                self.save_data()
                popup.dismiss()
                self.show_goals()

            except (ValueError, IndexError):
                status.text = "Enter a valid amount"

        add_button.bind(on_release=add_money)

        popup.open()

    # -------------------------
    # DELETE GOAL
    # -------------------------

    def confirm_delete_goal(self, index):

        content = BoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=dp(12)
        )

        content.add_widget(
            Label(text="Delete this savings goal?")
        )

        buttons = BoxLayout(
            spacing=dp(10),
            size_hint_y=None,
            height=dp(45)
        )

        cancel_button = Button(text="CANCEL")

        delete_button = Button(
            text="DELETE",
            background_normal="",
            background_color=(0.55, 0.2, 0.2, 1)
        )

        buttons.add_widget(cancel_button)
        buttons.add_widget(delete_button)
        content.add_widget(buttons)

        popup = Popup(
            title="Confirm deletion",
            content=content,
            size_hint=(0.85, 0.3)
        )

        def delete_goal(*args):

            if 0 <= index < len(self.goals):
                self.goals.pop(index)

                self.save_data()

            popup.dismiss()
            self.show_goals()

        cancel_button.bind(
            on_release=lambda button: popup.dismiss()
        )

        delete_button.bind(
            on_release=delete_goal
        )

        popup.open()
    # -------------------------
    # STATISTICS SCREEN
    # -------------------------

    def show_statistics(self):

        self.current_screen = "statistics"
        self.update_navigation()
        self.content.clear_widgets()

        screen = BoxLayout(
            orientation="vertical",
            spacing=dp(10)
        )

        screen.add_widget(
            Label(
                text="MONTHLY STATISTICS",
                font_size=18,
                color=(0.35, 0.85, 0.65, 1),
                size_hint_y=None,
                height=dp(40)
            )
        )

        months = set()

        for item in self.transactions:

            try:
                date = datetime.strptime(
                    item.get("date", ""),
                    "%d.%m.%Y %H:%M"
                )

                months.add(date.strftime("%m.%Y"))

            except (ValueError, TypeError):
                continue

        current_month = datetime.now().strftime("%m.%Y")
        months.add(current_month)

        self.month_keys = sorted(
            months,
            key=lambda x: datetime.strptime(x, "%m.%Y"),
            reverse=True
        )

        self.month_names = {}

        for month in self.month_keys:

            display_name = datetime.strptime(
                month, "%m.%Y"
            ).strftime("%B %Y")

            self.month_names[display_name] = month

        selected_name = datetime.strptime(
            self.month_keys[0], "%m.%Y"
        ).strftime("%B %Y")

        self.selected_month = self.month_keys[0]

        self.month_spinner = Spinner(
            text=selected_name,
            values=list(self.month_names.keys()),
            size_hint_y=None,
            height=dp(45)
        )

        self.month_spinner.bind(
            text=self.change_month
        )

        screen.add_widget(self.month_spinner)
        self.limits_button = Button(
            text="MANAGE SPENDING LIMITS",
            size_hint_y=None,
            height=dp(45),
            background_normal="",
            background_color=(0.2, 0.65, 0.45, 1)
        )

        self.limits_button.bind(
            on_release=lambda x: self.open_limits()
        )

        screen.add_widget(self.limits_button)

        self.total_income_label = Label(
            text="Monthly income: 0 KZT",
            font_size=16,
            bold=True,
            color=(0.35, 0.85, 0.65, 1),
            size_hint_y=None,
            height=dp(35)
        )

        self.total_expenses_label = Label(
            text="Monthly expenses: 0 KZT",
            font_size=16,
            bold=True,
            color=(1, 0.45, 0.45, 1),
            size_hint_y=None,
            height=dp(35)
        )

        self.net_balance_label = Label(
            text="Net balance: 0 KZT",
            font_size=17,
            bold=True,
            color=(0.35, 0.85, 0.65, 1),
            size_hint_y=None,
            height=dp(40)
        )

        screen.add_widget(self.total_income_label)
        screen.add_widget(self.total_expenses_label)
        screen.add_widget(self.net_balance_label)
        scroll = ScrollView(
            do_scroll_x=False
        )

        self.stats_box = BoxLayout(
            orientation="vertical",
            spacing=dp(12),
            size_hint_y=None
        )

        self.stats_box.bind(
            minimum_height=self.stats_box.setter("height")
        )

        scroll.add_widget(self.stats_box)
        screen.add_widget(scroll)

        self.content.add_widget(screen)

        self.update_statistics()

    def change_month(self, spinner, text):

        if text not in self.month_names:
            return

        self.selected_month = self.month_names[text]

        self.update_statistics()

    def update_statistics(self):

        if not hasattr(self, "stats_box"):
            return

        self.stats_box.clear_widgets()

        category_totals = {}
        total_expenses = 0.0
        total_income = 0.0

        for item in self.transactions:

            try:
                date = datetime.strptime(
                    item.get("date", ""),
                    "%d.%m.%Y %H:%M"
                )
            except (ValueError, TypeError):
                continue

            if date.strftime("%m.%Y") != self.selected_month:
                continue

            amount = float(item.get("amount", 0))
            kind = item.get("kind")

            if kind == "income":

                total_income += amount

            elif kind == "expense":

                total_expenses += amount
                category = item.get("category", "Other")

                if category not in category_totals:
                    category_totals[category] = 0.0

                category_totals[category] += amount

        net_balance = total_income - total_expenses

        self.total_income_label.text = (
            f"Monthly income: {total_income:,.2f} {self.get_currency_symbol()}"
        )

        self.total_expenses_label.text = (
            f"Monthly expenses: {total_expenses:,.2f} {self.get_currency_symbol()}"
        )

        self.net_balance_label.text = (
            f"Net balance: {net_balance:,.2f} {self.get_currency_symbol()}"
        )

        self.total_expenses_label.text = (
            f"Total expenses: {total_expenses:,.2f} {self.get_currency_symbol()}"
        )

        # SPENDING LIMITS DISPLAY
        limits_title = Label(
            text="SPENDING LIMITS",
            font_size=16,
            bold=True,
            color=(0.35, 0.85, 0.65, 1),
            size_hint_y=None,
            height=dp(35)
        )

        self.stats_box.add_widget(limits_title)

        if not self.limits:

            self.stats_box.add_widget(
                Label(
                    text="No spending limits set",
                    color=(0.5, 0.55, 0.55, 1),
                    size_hint_y=None,
                    height=dp(35)
                )
            )

        for category, limit in self.limits.items():

            spent = category_totals.get(category, 0.0)

            percentage = spent / limit * 100
            remaining = limit - spent

            row = BoxLayout(
                orientation="vertical",
                spacing=dp(5),
                size_hint_y=None,
                height=dp(75)
            )

            label = Label(
                text=(
                    f"{category}: "
                    f"{spent:,.0f} / {limit:,.0f} KZT "
                    f"({percentage:.1f}%)"
                ),
                color=(
                    (1, 0.4, 0.4, 1)
                    if percentage >= 100
                    else (0.8, 0.85, 0.85, 1)
                ),
                font_size=13,
                size_hint_y=None,
                height=dp(28)
            )

            bar = MintProgressBar(
                percentage=min(percentage, 100),
                size_hint_y=None,
                height=dp(12)
            )

            remaining_label = Label(
                text=(
                    f"Over limit: {abs(remaining):,.0f} {self.get_currency_symbol()}"
                    if remaining < 0
                    else f"Remaining: {remaining:,.0f} {self.get_currency_symbol()}"
                ),
                color=(0.35, 0.85, 0.65, 1)
                if remaining >= 0
                else (1, 0.4, 0.4, 1),
                font_size=12,
                size_hint_y=None,
                height=dp(25)
            )

            row.add_widget(label)
            row.add_widget(bar)
            row.add_widget(remaining_label)

            self.stats_box.add_widget(row)
        if not category_totals:

            self.stats_box.add_widget(
                Label(
                    text="No expenses this month",
                    color=(0.5, 0.55, 0.55, 1),
                    size_hint_y=None,
                    height=dp(50)
                )
            )

            return

        sorted_categories = sorted(
            category_totals.items(),
            key=lambda x: x[1],
            reverse=True
        )

        for category, amount in sorted_categories:

            percentage = amount / total_expenses * 100

            row = BoxLayout(
                orientation="vertical",
                spacing=dp(5),
                size_hint_y=None,
                height=dp(60)
            )

            label = Label(
                text=(
                    f"{category}: {amount:,.2f} KZT "
                    f"({percentage:.1f}%)"
                ),
                color=(0.8, 0.85, 0.85, 1),
                font_size=13,
                halign="left",
                valign="middle",
                size_hint_y=None,
                height=dp(28)
            )

            label.bind(
                size=lambda instance, value:
                setattr(instance, "text_size", value)
            )

            bar = MintProgressBar(
                percentage=percentage,
                size_hint_y=None,
                height=dp(12)
            )

            row.add_widget(label)
            row.add_widget(bar)

            self.stats_box.add_widget(row)
    # -------------------------
    # SPENDING LIMITS
    # -------------------------

    def open_limits(self):

        content = BoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=dp(12)
        )

        category_spinner = Spinner(
            text=EXPENSE_CATEGORIES[0],
            values=EXPENSE_CATEGORIES,
            size_hint_y=None,
            height=dp(48)
        )

        amount_input = TextInput(
            hint_text="Monthly limit in KZT",
            multiline=False,
            input_filter="float",
            size_hint_y=None,
            height=dp(48)
        )

        status = Label(
            text="",
            color=(1, 0.4, 0.4, 1)
        )

        def load_limit(spinner, category):
            amount_input.text = str(
                self.limits.get(category, "")
            )

        category_spinner.bind(
            text=load_limit
        )

        save_button = Button(
            text="SAVE LIMIT",
            size_hint_y=None,
            height=dp(48),
            background_normal="",
            background_color=(0.2, 0.65, 0.45, 1)
        )

        content.add_widget(category_spinner)
        content.add_widget(amount_input)
        content.add_widget(status)
        content.add_widget(save_button)

        popup = Popup(
            title="SPENDING LIMIT",
            content=content,
            size_hint=(0.88, 0.48)
        )

        def save_limit(*args):

            try:
                amount = float(
                    amount_input.text.replace(",", ".")
                )

                if amount <= 0:
                    raise ValueError

                category = category_spinner.text

                self.limits[category] = amount

                self.save_data()
                self.update_statistics()

                popup.dismiss()

            except ValueError:
                status.text = "Enter a valid amount"

        save_button.bind(
            on_release=save_limit
        )

        delete_button = Button(
            text="DELETE LIMIT",
            size_hint_y=None,
            height=dp(42),
            background_normal="",
            background_color=(0.65, 0.2, 0.2, 1)
        )

        def confirm_delete(*args):

            category = category_spinner.text

            if category not in self.limits:
                status.text = "No limit for this category"
                return

            confirm_content = BoxLayout(
                orientation="vertical",
                spacing=dp(10),
                padding=dp(12)
            )

            confirm_content.add_widget(
                Label(
                    text=f"Delete limit for {category}?"
                )
            )

            confirm_buttons = BoxLayout(
                spacing=dp(10),
                size_hint_y=None,
                height=dp(45)
            )

            confirm_popup = Popup(
                title="CONFIRM DELETE",
                content=confirm_content,
                size_hint=(0.85, 0.3)
            )

            cancel_button = Button(text="CANCEL")
            yes_button = Button(
                text="DELETE",
                background_normal="",
                background_color=(0.65, 0.2, 0.2, 1)
            )

            cancel_button.bind(
                on_release=confirm_popup.dismiss
            )

            def delete_limit(*args):

                self.limits.pop(category, None)
                self.save_data()
                confirm_popup.dismiss()
                popup.dismiss()
                self.update_statistics()

            yes_button.bind(
                on_release=delete_limit
            )

            confirm_buttons.add_widget(cancel_button)
            confirm_buttons.add_widget(yes_button)
            confirm_content.add_widget(confirm_buttons)

            confirm_popup.open()

        delete_button.bind(
            on_release=confirm_delete
        )

        content.add_widget(delete_button)

        popup.open()
    # -------------------------
    # GOALS SCREEN
    # -------------------------

    def show_goals(self):

        self.current_screen = "goals"
        self.update_navigation()
        self.content.clear_widgets()

        screen = BoxLayout(
            orientation="vertical",
            spacing=dp(10)
        )

        screen.add_widget(
            Label(
                text="SAVINGS GOALS",
                font_size=18,
                color=(0.35, 0.85, 0.65, 1),
                size_hint_y=None,
                height=dp(40)
            )
        )

        add_button = Button(
            text="+ NEW GOAL",
            size_hint_y=None,
            height=dp(48),
            background_normal="",
            background_color=(0.2, 0.65, 0.45, 1)
        )

        add_button.bind(
            on_release=lambda x: self.open_goal_popup()
        )

        screen.add_widget(add_button)

        scroll = ScrollView(
            do_scroll_x=False
        )

        self.goals_box = BoxLayout(
            orientation="vertical",
            spacing=dp(15),
            size_hint_y=None
        )

        self.goals_box.bind(
            minimum_height=self.goals_box.setter("height")
        )

        scroll.add_widget(self.goals_box)
        screen.add_widget(scroll)

        self.content.add_widget(screen)

        self.update_goals()

    def update_goals(self):

        self.goals_box.clear_widgets()

        if not self.goals:

            self.goals_box.add_widget(
                Label(
                    text=(
                        "You have no savings goals yet.\n"
                        "Create your first goal!"
                    ),
                    color=(0.6, 0.65, 0.65, 1),
                    size_hint_y=None,
                    height=dp(100)
                )
            )

            return

        for index, goal in enumerate(self.goals):

            target = float(goal["target"])
            saved = float(goal["saved"])

            percentage = (
                saved / target * 100
                if target > 0
                else 0
            )

            remaining = max(0, target - saved)

            card = BoxLayout(
                orientation="vertical",
                spacing=dp(8),
                padding=dp(12),
                size_hint_y=None,
                height=dp(190)
            )

            with card.canvas.before:
                Color(0.10, 0.13, 0.13, 1)

                card.background = RoundedRectangle(
                    pos=card.pos,
                    size=card.size,
                    radius=[dp(10)]
                )

            card.bind(
                pos=lambda instance, value:
                setattr(instance.background, "pos", value)
            )

            card.bind(
                size=lambda instance, value:
                setattr(instance.background, "size", value)
            )

            name_label = Label(
                text=goal["name"],
                font_size=17,
                bold=True,
                color=(0.35, 0.85, 0.65, 1),
                halign="left",
                size_hint_y=None,
                height=dp(30)
            )

            amount_label = Label(
                text=(
                    f"{saved:,.2f} / {target:,.2f} {self.get_currency_symbol()}"
                ),
                font_size=14,
                color=(1, 1, 1, 1),
                size_hint_y=None,
                height=dp(25)
            )

            progress_label = Label(
                text=f"{percentage:.1f}% completed",
                font_size=12,
                color=(0.65, 0.7, 0.7, 1),
                size_hint_y=None,
                height=dp(22)
            )

            bar = MintProgressBar(
                percentage=min(percentage, 100),
                size_hint_y=None,
                height=dp(12)
            )

            remaining_label = Label(
                text=f"Remaining: {remaining:,.2f} {self.get_currency_symbol()}",
                font_size=12,
                color=(0.65, 0.7, 0.7, 1),
                size_hint_y=None,
                height=dp(22)
            )

            buttons = BoxLayout(
                spacing=dp(8),
                size_hint_y=None,
                height=dp(38)
            )

            add_money = Button(
                text="+ ADD MONEY",
                background_normal="",
                background_color=(0.2, 0.55, 0.4, 1)
            )

            delete = Button(
                text="DELETE",
                background_normal="",
                background_color=(0.45, 0.2, 0.2, 1)
            )

            add_money.bind(
                on_release=lambda button, i=index:
                self.open_add_money(i)
            )

            delete.bind(
                on_release=lambda button, i=index:
                self.confirm_delete_goal(i)
            )

            buttons.add_widget(add_money)
            buttons.add_widget(delete)

            card.add_widget(name_label)
            card.add_widget(amount_label)
            card.add_widget(progress_label)
            card.add_widget(bar)
            card.add_widget(remaining_label)
            card.add_widget(buttons)

            self.goals_box.add_widget(card)

    # -------------------------
    # CREATE GOAL
    # -------------------------

    def open_goal_popup(self):

        content = BoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=dp(12)
        )

        name_input = TextInput(
            hint_text="Goal name",
            multiline=False,
            size_hint_y=None,
            height=dp(48)
        )

        target_input = TextInput(
            hint_text=f"Target amount in {self.get_currency_symbol()}",
            multiline=False,
            input_filter="float",
            size_hint_y=None,
            height=dp(48)
        )

        status = Label(
            text="",
            color=(1, 0.4, 0.4, 1)
        )

        save_button = Button(
            text="CREATE GOAL",
            size_hint_y=None,
            height=dp(48),
            background_normal="",
            background_color=(0.2, 0.65, 0.45, 1)
        )

        content.add_widget(name_input)
        content.add_widget(target_input)
        content.add_widget(status)
        content.add_widget(save_button)

        popup = Popup(
            title="New savings goal",
            content=content,
            size_hint=(0.88, 0.55)
        )

        def create_goal(*args):

            name = name_input.text.strip()

            try:
                target = float(
                    target_input.text.replace(",", ".")
                )

                if not name:
                    status.text = "Enter a goal name"
                    return

                if target <= 0:
                    status.text = "Enter a positive amount"
                    return

                self.goals.append({
                    "name": name,
                    "target": target,
                    "saved": 0.0
                })

                self.save_data()
                popup.dismiss()
                self.show_goals()

            except ValueError:
                status.text = "Enter a valid amount"
        save_button.bind(on_release=create_goal)
        popup.open()


    # -------------------------
    # SETTINGS SCREEN
    # -------------------------

    def show_settings(self):

        self.current_screen = "settings"
        self.update_navigation()
        self.content.clear_widgets()

        screen = BoxLayout(
            orientation="vertical",
            spacing=dp(12),
            padding=dp(15)
        )

        screen.add_widget(
            Label(
                text="SETTINGS",
                font_size=22,
                bold=True,
                color=(0.35, 0.85, 0.65, 1),
                size_hint_y=None,
                height=dp(45)
            )
        )

        screen.add_widget(
            Label(
                text="APP INFORMATION",
                font_size=16,
                bold=True,
                color=(0.35, 0.85, 0.65, 1),
                size_hint_y=None,
                height=dp(35)
            )
        )

        screen.add_widget(
            Label(
                text="MINT Finance Tracker\nVersion 1.0\nPersonal Finance Management",
                font_size=14,
                color=(0.8, 0.85, 0.85, 1),
                size_hint_y=None,
                height=dp(85)
            )
        )

        screen.add_widget(
            Label(
                text="CURRENCY",
                font_size=16,
                bold=True,
                color=(0.35, 0.85, 0.65, 1),
                size_hint_y=None,
                height=dp(35)
            )
        )

        currency_spinner = Spinner(
            text=self.currency,
            values=("KZT", "USD", "EUR"),
            size_hint_y=None,
            height=dp(45)
        )

        screen.add_widget(currency_spinner)

        currency_status = Label(
            text="",
            color=(0.35, 0.85, 0.65, 1),
            size_hint_y=None,
            height=dp(30)
        )

        screen.add_widget(currency_status)

        save_currency_button = Button(
            text="SAVE CURRENCY",
            size_hint_y=None,
            height=dp(45),
            background_normal="",
            background_color=(0.2, 0.65, 0.45, 1)
        )

        def save_currency(*args):

            self.currency = currency_spinner.text
            self.save_data()

            currency_status.text = (
                "Currency saved: " + self.currency
            )

        save_currency_button.bind(
            on_release=save_currency
        )

        screen.add_widget(save_currency_button)

        screen.add_widget(
            Label(
                text="DATA MANAGEMENT",
                font_size=16,
                bold=True,
                color=(0.35, 0.85, 0.65, 1),
                size_hint_y=None,
                height=dp(35)
            )
        )

        screen.add_widget(
            Label(
                text="Your financial data is stored locally.",
                font_size=14,
                color=(0.8, 0.85, 0.85, 1),
                size_hint_y=None,
                height=dp(40)
            )
        )

        self.content.add_widget(screen)
import traceback

try:
    MintApp().run()
except Exception:
    with open("/storage/emulated/0/mint_error.txt", "w") as f:
        f.write(traceback.format_exc())
    raise
