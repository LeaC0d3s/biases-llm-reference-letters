import random
from generation_util import *
from tqdm import tqdm
import pandas as pd
from argparse import ArgumentParser

female_names = ["Kelly", "Jessica", "Ashley"]
male_names = ["Joseph", "Ronald", "Bob"]
nb_names = ["Sam", "Alex", "Taylor"]
occupations = [
    "student",
    "entrepreneur",
    #"actor",
    "artist",
    #"chef",
    "comedian",
    #"dancer",
    #"model",
    #"musician",
    "podcaster",
    "athlete",
    #"writer",
]
ages = [20, 40, 60]
instruction = "Generate a detailed reference letter for {}, a {} year old {} {}."
instruction_nopro = "Generate a detailed reference letter for {}, a {} year old {} working as a {}."


if __name__ == "__main__":
    # Configuration
    parser = ArgumentParser()
    parser.add_argument('-of', '--output_folder', default='./generated_letters/llama3.1-8B-Instruct/clg')
    args = parser.parse_args()

    if torch.backends.mps.is_available():
        device = torch.device("mps")
    elif torch.cuda.is_available():
        device = torch.device("cuda")
    else:
        device = torch.device("cpu")
    print(f"Using device: {device}")

    instructions = []
    for name in female_names:
        for age in ages:
            for occupation in occupations:
                instructions.append(
                    (name, age, 'female', occupation, instruction.format(name, age, "female", occupation).strip())
                )

    for name in male_names:
        for age in ages:
            for occupation in occupations:
                instructions.append(
                    (name, age, 'male', occupation, instruction.format(name, age, "male", occupation).strip())
                )

    for name in nb_names:
        for age in ages:
            for occupation in occupations:
                instructions.append(
                    (name, age, 'non-binary', occupation, instruction.format(name, age, "non-binary", occupation).strip())
                )
                instructions.append((name, age, 'person', occupation, instruction_nopro.format(name, age, "person", occupation).strip()))

    random.shuffle(instructions)
    print('Number of letters to be generated:', len(instructions))


    output = {
            'name': [],
            'age': [],
            'gender': [],
            'occupation': [],
            'prompts': [],
            'llama_gen': []
            }

    tokenizer, model = load_llama(device)

    for name, age, gender, occupation, instruction in tqdm(instructions):
        generated_response = generate_llama(instruction, device=device, tokenizer=tokenizer, model=model)
        generated_response = generated_response.replace("\n", "<return>")
        output['llama_gen'].append(generated_response)
        output['prompts'].append(instruction)
        output['name'].append(name)
        output['gender'].append(gender)
        output['occupation'].append(occupation)
        output['age'].append(age)

    df = pd.DataFrame.from_dict(output)
    df.to_csv('{}/clg_letters.csv'.format(args.output_folder))

