import os

from data_processing_flows import generate_flow


def main():
    flow = generate_flow(os.path.abspath(os.path.join(os.path.dirname(__file__), "flow_example.json")))
    print(flow)
    flow.execute()

if __name__ == "__main__":
    main()
