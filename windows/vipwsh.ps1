if (get-command nvim -ErrorAction SilentlyContinue) {
    nvim $Profile.AllUsersCurrentHost
} else {
    notepad $Profile.AllUsersCurrentHost
}
