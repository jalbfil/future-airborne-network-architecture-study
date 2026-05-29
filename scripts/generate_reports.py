from future_airborne_network_study.reports import generate_all_reports


def main() -> None:
    for path in generate_all_reports():
        print(f"Generated {path}")


if __name__ == "__main__":
    main()
