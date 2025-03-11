import pickle

try:
    with open('trained_agents_data.pkl', 'rb') as file:
        data = pickle.load(file)
    print("File loaded successfully.")
except Exception as e:
    print(f"An error occurred: {e}")