from rag_pipeline import answer_query


def main():
    print("🎓 Scholarship RAG Assistant")
    print("Type 'exit' to quit.\n")

    while True:
        query = input("You: ")

        if query.lower() in ["exit", "quit"]:
            print("Goodbye ")
            break

        print("\nSearching...\n")

        response = answer_query(query)

        print("Assistant:\n")
        print(response)
        print("\n" + "-" * 80 + "\n")


if __name__ == "__main__":
    main()