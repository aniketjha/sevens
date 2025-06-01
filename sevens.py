import random
from collections import defaultdict

SUITS = ['♠', '♥', '♦', '♣']
RANKS = list(range(1, 14))  # 1=Ace, 11=Jack, 12=Queen, 13=King

# Create full deck of cards
def create_deck():
    return [(rank, suit) for suit in SUITS for rank in RANKS]

# Represent card nicely
def card_str(card):
    rank, suit = card
    name_map = {1: 'A', 11: 'J', 12: 'Q', 13: 'K'}
    rank_str = name_map.get(rank, str(rank))
    return f"{rank_str}{suit}"

# Check if a card is playable
def is_playable(card, table):
    rank, suit = card
    if rank == 7:
        return True
    if suit in table:
        min_rank = min(table[suit])
        max_rank = max(table[suit])
        return rank == min_rank - 1 or rank == max_rank + 1
    return False

# Add card to the table
def play_card(card, table):
    rank, suit = card
    if suit not in table:
        table[suit] = [rank]
    else:
        table[suit].append(rank)
        table[suit].sort()

# Print current table
def display_table(table):
    print("\n📋 Table:")
    for suit in SUITS:
        ranks = table.get(suit, [])
        if ranks:
            cards = [card_str((r, suit)) for r in sorted(ranks)]
            print(f"{suit}: {' '.join(cards)}")
        else:
            print(f"{suit}: (empty)")
    print()

# Game setup
def deal_cards(deck, num_players):
    random.shuffle(deck)
    return [deck[i::num_players] for i in range(num_players)]

# Player turn
def player_turn(player_cards, table):
    print("\nYour cards:")
    playable = []
    for i, card in enumerate(player_cards):
        if is_playable(card, table):
            playable.append((i, card))
            print(f"{i+1}. {card_str(card)} (playable)")
        else:
            print(f"{i+1}. {card_str(card)}")

    if playable:
        choice = input("Enter card number to play or 'p' to pass: ")
        if choice.lower() == 'p':
            return None
        try:
            index = int(choice) - 1
            if index in [i for i, _ in playable]:
                return player_cards.pop(index)
        except:
            pass
        print("❌ Invalid input. You passed this round.")
        return None
    else:
        print("🚫 No playable cards. You pass.")
        return None

# AI turn
def ai_turn(ai_cards, table):
    for i, card in enumerate(ai_cards):
        if is_playable(card, table):
            return ai_cards.pop(i)
    return None

# Game loop
def play_sevens():
    num_players = 4
    player_names = ["You", "Bot 1", "Bot 2", "Bot 3"]
    deck = create_deck()
    hands = deal_cards(deck, num_players)
    table = defaultdict(list)
    finished = [False] * num_players

    print("🃏 Welcome to Sevens!\n")

    while not all(finished):
        for i in range(num_players):
            if finished[i]:
                continue
            name = player_names[i]
            print(f"\n🎮 {name}'s turn")
            display_table(table)

            card = None
            if name == "You":
                card = player_turn(hands[i], table)
            else:
                card = ai_turn(hands[i], table)
                if card:
                    print(f"{name} played: {card_str(card)}")
                else:
                    print(f"{name} passes.")

            if card:
                play_card(card, table)

            if not hands[i]:
                finished[i] = True
                print(f"🏁 {name} has finished all cards!")

    print("\n🎉 Game Over!")
    print("📊 Final Rankings:")
    for i, name in enumerate(player_names):
        print(f"{name}: {'Done' if finished[i] else f'{len(hands[i])} cards left'}")

if __name__ == "__main__":
    play_sevens()# sevens
