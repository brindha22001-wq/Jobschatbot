from app.preprocessing.clean_data import clean_jobs_data


if __name__ == "__main__":
    output = clean_jobs_data()
    print(f"Cleaned file generated at: {output}")
