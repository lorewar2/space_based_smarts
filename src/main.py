
import start_menu
import level_selection
import main_screen

def main():
    main_screen.run_map(0, 0)
    start_state = start_menu.start_menu()
    if start_state == True:
        # run the selection menu
        print("next section")
        level_state = level_selection.selection_menu()
        if level_state == (-1, -1):
            return
        print(level_state)
    
       
    else:
        return
    
 
if __name__ == "__main__":
    main()
