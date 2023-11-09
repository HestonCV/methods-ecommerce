# - databaseName: string
# - tableName: string
# - loggedIn: bool
# - userID: string
# + User()
# + User(string databaseName, string tableName)
# + login(): bool
# + logout(): bool
# + viewAccountInformation(): void
# + createAccount(): void
# + getLoggedIn(): bool
# + getUserID(): string