from photon.menu import Menu, Keyboard, Button
from photon.state import state_back


main_menu_keyboard = Keyboard([
    [ Button("calculate 1 + 2", lambda: f"result: {1 + 2}") ],
    [ Button("go to second menu", lambda: second_menu.call()) ],
    [ Button("go to", lambda state: state.back("back")) ],
])
main_menu = Menu(
    "Main Menu",
    main_menu_keyboard
)

second_menu = Menu(
    "Second Menu",
    Keyboard([
        [ Button("Back", state_back) ]
    ])
)

