
import start_menu
import level_selection

def main():
    level_selection.selection_menu()
    start_state = start_menu.start_menu()
    if start_state == True:
        # run the next
        print("next section")

 
if __name__ == "__main__":
    main()
