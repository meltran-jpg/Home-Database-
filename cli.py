


# simple cli for interacting with the smart home database using natural language commands


from __future__ import annotations
from services.llm_adapter import nl_to_sql
from services.query_service import run_query
# helper function to print query results in a user way for the cli
def _print_results(response: dict)-> None:
    # print query results for the cli
    if not response["ok"]:
        print(f"error: {response['error']}")
        return
# if there are results from a select query -->print them in a readable format
    if response["results"]:
        for row in response["results"]:
            print(row)
        return
    # for non select queries --> print success and number of rows affected
    print(f"success! rows affected: {response.get('rows_affected', 0)}")
# main loop for the cli -->prompt user for input -->translate to sql-->run query-->and print results
def main() -> None:
    print("smart home db cli")
    print("type 'exit' or 'quit' to stop.")
    # loop to continuously prompt the user for nl commands until they choose to exit
    while True:
        user_input = input("enter command: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            print("goodbye!")
            break
        sql_command = nl_to_sql(user_input)
        response = run_query(sql_command)
        _print_results(response)

if __name__ == "__main__":
    main()