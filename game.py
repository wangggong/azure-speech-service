from enum import Enum
import random
import uuid

class Component(Enum):
    BACKEND = 1
    FRONTEND = 2
    ALGORITHM = 3
    INFRASTRUCTURE = 4


class Severity(Enum):
    SEV1 = "Sev1"
    SEV2 = "Sev2"
    SEV3 = "Sev3"
    NO_INCIDENT = "NoIncident"


class CardType(Enum):
    KNOWN_BUG = 1
    TRANSIENT = 2
    INVESTIGATE = 3
    CHECK_BACKLOG = 4
    REQUEST_HELP = 5
    WORK_AROUND = 6
    REOPEN = 7
    ROOT_CAUSE_ANALYSIS = 8
    TRANSFER = 9
    ESCALATE = 10
    DOWNGRADE = 11


class GameState(Enum):
    PREPARE_GAME = -1
    GAME_START = 0
    DRAW_PHASE = 1
    PLAY_PHASE = 2
    RESOLVE_PHASE = 3
    GAME_END = 4


class PlayerState(Enum):
    GAMING = 0
    WIN = 1
    LOSE = 2

class Incident:
    incident_deck = []
    id_counter = 1

    def __init__(self, component, severity):
        self.id = Incident.id_counter
        Incident.id_counter += 1
        self.component = component
        self.severity = severity

    def __str__(self):
        if self.severity == Severity.NO_INCIDENT:
            return f"ID: {self.id} - No incident"
        else:
            return f"ID: {self.id} - {self.severity.value} incident in {self.component.name.lower()}"

    def __repr__(self):
        return f"Incident({self.component}, {self.severity}, {self.id})"

    @staticmethod
    def init_incidents():
        for component in Component:
            for _ in range(1):
                Incident.incident_deck.append(Incident(component, Severity.SEV1))
            for _ in range(3):
                Incident.incident_deck.append(Incident(component, Severity.SEV2))
            for _ in range(9):
                Incident.incident_deck.append(Incident(component, Severity.SEV3))
        for _ in range(4):
            Incident.incident_deck.append(Incident(None, Severity.NO_INCIDENT))
        random.shuffle(Incident.incident_deck)
        return Incident.incident_deck


class Card:
    card_deck = []
    CARD_COUNTS = {
        CardType.TRANSIENT: 6,
        CardType.INVESTIGATE: 4,
        CardType.CHECK_BACKLOG: 4,
        CardType.REQUEST_HELP: 6,
        CardType.WORK_AROUND: 6,
        CardType.REOPEN: 4,
        CardType.ROOT_CAUSE_ANALYSIS: 4,
        CardType.TRANSFER: 6,
        CardType.ESCALATE: 4,
        CardType.DOWNGRADE: 4,
    }
    id_counter = 1

    def __init__(self, card_type):
        self.id = Card.id_counter
        Card.id_counter += 1
        self.card_type = card_type

    def __str__(self):
        return f"ID: {self.id} - {self.card_type.name}"

    def __repr__(self):
        return f"{self.id}: {self.__class__.__name__}(CardType.{self.card_type.name})"

    def usage(self, game_state):
        raise NotImplementedError("Subclasses must implement usage method")

    @staticmethod
    def init_cards():
        for card_type, count in Card.CARD_COUNTS.items():
            if card_type == CardType.KNOWN_BUG:
                continue
            for _ in range(count):
                Card.card_deck.append(CardFactory.create_card(card_type))
        Card.card_deck.extend(KnownBugCard.init_known_bugs())
        random.shuffle(Card.card_deck)
        return Card.card_deck


class KnownBugCard(Card):
    def __init__(self, component):
        super().__init__(CardType.KNOWN_BUG)
        self.component = component

    @staticmethod
    def init_known_bugs():
        known_bugs = []
        for component in Component:
            for _ in range(9):
                known_bugs.append(KnownBugCard(component))
        return known_bugs


class TransientCard(Card):
    def __init__(self):
        super().__init__(CardType.TRANSIENT)

class InvestigateCard(Card):
    def __init__(self):
        super().__init__(CardType.INVESTIGATE)

class CheckBacklogCard(Card):
    def __init__(self):
        super().__init__(CardType.CHECK_BACKLOG)

class RequestHelpCard(Card):
    def __init__(self):
        super().__init__(CardType.REQUEST_HELP)

class WorkAroundCard(Card):
    def __init__(self):
        super().__init__(CardType.WORK_AROUND)

class ReopenCard(Card):
    def __init__(self):
        super().__init__(CardType.REOPEN)

class RootCauseAnalysisCard(Card):
    def __init__(self):
        super().__init__(CardType.ROOT_CAUSE_ANALYSIS)

class TransferCard(Card):
    def __init__(self):
        super().__init__(CardType.TRANSFER)

class EscalateCard(Card):
    def __init__(self):
        super().__init__(CardType.ESCALATE)

class DowngradeCard(Card):
    def __init__(self):
        super().__init__(CardType.DOWNGRADE)


class CardFactory:
    @staticmethod
    def create_card(card_type):
        if card_type == CardType.KNOWN_BUG:
            return KnownBugCard.init_known_bugs()
        elif card_type == CardType.TRANSIENT:
            return TransientCard()
        elif card_type == CardType.INVESTIGATE:
            return InvestigateCard()
        elif card_type == CardType.CHECK_BACKLOG:
            return CheckBacklogCard()
        elif card_type == CardType.REQUEST_HELP:
            return RequestHelpCard()
        elif card_type == CardType.WORK_AROUND:
            return WorkAroundCard()
        elif card_type == CardType.REOPEN:
            return ReopenCard()
        elif card_type == CardType.ROOT_CAUSE_ANALYSIS:
            return RootCauseAnalysisCard()
        elif card_type == CardType.TRANSFER:
            return TransferCard()
        elif card_type == CardType.ESCALATE:
            return EscalateCard()
        elif card_type == CardType.DOWNGRADE:
            return DowngradeCard()
        else:
            raise ValueError(f"Invalid card type: {card_type}")


class Player:
    def __init__(self, alias):
        self.alias = alias
        self.current_state = PlayerState.GAMING
        self.cards = []
        self.incidents = []

    def add_card(self, card):
        self.cards.append(card)

    def add_incident(self, incident):
        self.incidents.append(incident)

    def __str__(self):
        return self.alias

    def __repr__(self):
        return f"Player(alias={self.alias}, state={self.current_state})"


class Game:
    def __init__(self, player_count):
        self.id = str(uuid.uuid4())
        self.incidents = Incident.init_incidents()
        self.cards = Card.init_cards()
        self.players = []
        self.player_count = player_count
        self.current_state = GameState.PREPARE_GAME

    def set_state(self, next_state):
        # TODO state machine valid check
        self.current_state = next_state

    def add_player(self, player):
        assert self.current_state == GameState.PREPARE_GAME, 'invalid state: ' + self.current_state
        assert len(self.player) < self.player_count, 'invalid player count'
        assert not any(p for p in self.player if self.player.alias == player.alias)
        self.players.append(player)
        if len(self.players) == self.player_count:
            self.set_state(GameState.GAME_START)

    def start(self):
        # Initialize the deck of cards
        self.cards = Card.init_cards()
        self.game_loop()

    def game_loop(self):
        # TODO
        pass

    def __str__(self):
        return f"Game {self.id}:\ncards={self.cards}\nincidents={self.incidents}\ncurrent_state={self.current_state}"

    def __repr__(self):
        return f"Game(id={self.id})"


if __name__ == '__main__':
    print(Game(5))
