# --- BASE CLASS ---
class StoryPhase:
    def __init__(self, title, description):
        self.title = title
        self.description = description

    def show_story(self):
        print(f"\n--- {self.title} ---")
        print(self.description)

# --- CHILD CLASSES ---
class UniversityPhase(StoryPhase):
    def show_story(self):
        print(f"\n--- {self.title} ---")
        print(self.description)

        choice = input("Should Via open up to Lark despite her 'perfect student' image? (yes/no): ").lower()

        if choice == "yes":
            print("Via opens up, and Lark discovers the real her beneath the surface.")
        elif choice == "no":
            print("Via keeps her walls up, but Lark continues to see through her.")
        else:
            print("Their connection grows quietly through shared moments.")

class GoldenPhase(StoryPhase):
    def show_story(self):
        print(f"\n--- {self.title} ---")
        print(self.description)

        choice = input("Should Via fully embrace her relationship with Lark? (yes/no): ").lower()

        if choice == "yes":
            print("They experience deep love filled with golden memories and quiet happiness.")
        elif choice == "no":
            print("Via holds back slightly, afraid of what the future may bring.")
        else:
            print("Their love blossoms naturally despite uncertainties.")

class ConflicPhase(StoryPhase):
    def show_story(self):
        print(f"\n--- {self.title} ---")
        print(self.description)

        choice = input("Should Via choose love over family expectations? (yes/no): ").lower()

        if choice == "yes":
            print("Via tries to fight for love, but the pressure from her family grows stronger.")
        elif choice == "no":
            print("Via prioritizes her responsibilities, slowly drifting away from Lark.")
        else:
            print("She struggles between duty and desire.")

class BreakupPhase(StoryPhase):
    def show_story(self):
        print(f"\n--- {self.title} ---")
        print(self.description)

        choice = input("Should Lark stay and fight for Via? (yes/no): ").lower()

        if choice == "yes":
            print("“Lark wants to stay, but realizes love alone is not enough at this time.")
        elif choice == "no":
            print("Lark lets her go, believing it's the best for her future.")
        else:
            print("Lark makes a painful decision in silence.")

        print("💔 They part ways despite still being deeply in love.")

class ReunionPhase(StoryPhase):
    def show_story(self):
        print(f"\n--- {self.title} ---")
        print(self.description)

        choice = input("Should Via and Lark reconnect when they meet again? (yes/no): ").lower()

        if choice == "yes":
            print("They reconnect and reflect on the love they once had.")
        elif choice == "no":
            print("They keep distance, but memories linger between them.")
        else:
            print("Their past quietly resurfaces in their present.")

class EndingPhase(StoryPhase):
    def show_story(self):
        print(f"\n--- {self.title} ---")
        print(self.description)

        input("Should Via and Lark try to rebuild their love? (yes/no): ").lower()

        print("\n---FINAL OUTCOME ---")
        print("Years later, Via becomes a successful Architect, and Lark becomes a visionary in his own path.")
        print("They meet again, no longer as the same people they once were.")
        print("They realize that their love was real, but it belonged to a different time.")
        print("The 'golden scenery' of their past remains beautiful, but their future is built with wisdom.")
        print("🌄 They move forward—whether together or apart—with acceptance and peace. 🌄")

#---STORY DEFINITION---
phase1 = UniversityPhase(
    "Phase 1: The University Days",
    "Via (UST) meets Lark (DLSU). Their connection begins through art, photography, and deepconversations."
)

phase2 = GoldenPhase(
    "Phase 2: The Golden Days",
    "Their relationship is filled with quiet, meaningful moments and emotional intimacy."
)

phase3 = ConflicPhase(
    "Phase 3: The Conflict",
    "Via faces pressure from her family, while Lark struggles with his own personal challenges."
)

phase4 = BreakupPhase(
    "Phase 4: The Breakup",
    "Lark makes the painful decision to let Via go for her future and growth."
)

phase5 = ReunionPhase(
    "Phase 5: The Reunion",
    "Years later, they meet again as professionals, carrying memories of their past."
)

phase6 = EndingPhase(
    "Phase 6: A New Horizon (Ending)",
    "They reflect on their past and decide how to move forward."
)

phases = [phase1, phase2, phase3, phase4, phase5, phase6]

#---MENU SYSTEM---
def run_story():
    while True:
        print("\n--- Story Phase ---")
        print("1 - University Days")
        print("2 - The Golder Days")
        print("3 - The Conflict")
        print("4 - The Breakup")
        print("5 - The Reunion")
        print("6 - A New Horizon Ending")
        print("7 - Exit")

        choice = input("Enter a phase number: ")

        if choice.isdigit():
            choice = float(choice)

            for a in range(len(phases)):
                if choice == a + 1:
                    phases[a].show_story()
                    break
            else:
                if choice == 7:
                    print("Exiting the story. Goodbye!")
                    break
                else:
                    print("Invalid choice. Please select from 1 to 7")
        else:
            print("Error: Please enter a valid number.")

if __name__ == "__main__":
 run_story()
