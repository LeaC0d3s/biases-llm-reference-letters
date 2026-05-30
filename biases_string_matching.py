import spacy
import pandas as pd
from tqdm import tqdm
from spacy.matcher import Matcher
from collections import Counter
from operator import itemgetter
import scipy.stats as stats
from argparse import ArgumentParser
import functools
import word_constants

if __name__ == '__main__':
    """
    Arguments:
    file_name: Directory of the input file.
    - For analyzing CLG letters, pass in './generated_letters/{model_type}/clg/clg_letters.csv'
    model_type: Model used to generated the letters.
    """
    parser = ArgumentParser()
    parser.add_argument('-f', '--file_name', type=str, default="./generated_letters/chatgpt/clg/clg_letters.csv")
    parser.add_argument('-m', '--model_type', default='chatgpt', required=False)
    parser.add_argument('-o', '--output', type=str, default=None, help='Write output to this file')
    args = parser.parse_args()
    rec_letters = pd.read_csv(args.file_name)
    INPUT = "{}_gen".format(args.model_type)

    output_file = open(args.output, 'w', encoding='utf-8') if args.output else None
    def output(*values, **kwargs):
        if output_file:
            print(*values, file=output_file, **kwargs)
        else:
            print(*values, **kwargs)

    if rec_letters['gender'][0] in ['male', 'female', 'non-binary', 'person']:
        rec_letters_m = rec_letters[rec_letters['gender'] == 'male']
        rec_letters_f = rec_letters[rec_letters['gender'] == 'female']
        rec_letters_nb = rec_letters[rec_letters['gender'] == 'non-binary']
        rec_letters_p = rec_letters[rec_letters['gender'] == 'person']
    else:
        rec_letters_m = rec_letters[rec_letters['gender'] == 'm']
        rec_letters_f = rec_letters[rec_letters['gender'] == 'f']
        rec_letters_nb = rec_letters[rec_letters['gender'] == 'nb']
        rec_letters_p = rec_letters[rec_letters['gender'] == 'p']

    # # generated letters
    rec_letters_m = rec_letters_m[INPUT].tolist()
    rec_letters_f = rec_letters_f[INPUT].tolist()
    rec_letters_nb = rec_letters_nb[INPUT].tolist()
    rec_letters_p = rec_letters_p[INPUT].tolist()

    ability_f, standout_f, masculine_f, feminine_f, agentic_f, communal_f, career_f, family_f, leader_f = 0, 0, 0, 0, 0, 0, 0, 0, 0
    ability_m, standout_m, masculine_m, feminine_m, agentic_m, communal_m, career_m, family_m, leader_m = 0, 0, 0, 0, 0, 0, 0, 0, 0
    ability_nb, standout_nb, masculine_nb, feminine_nb, agentic_nb, communal_nb, career_nb, family_nb, leader_nb = 0, 0, 0, 0, 0, 0, 0, 0, 0
    ability_p, standout_p, masculine_p, feminine_p, agentic_p, communal_p, career_p, family_p, leader_p = 0, 0, 0, 0, 0, 0, 0, 0, 0

    all_f, all_m, all_nb, all_p = 0, 0, 0, 0

    for i in tqdm(range(len(rec_letters_f)), ascii=True):
        rec_letter = rec_letters_f[i].split()
        n = len(rec_letter)
        all_f += n
        # For normal analysis
        for v in rec_letter:
            for w in word_constants.ABILITY_WORDS:
                if w in v.lower():
                    ability_f += 1
            for w in word_constants.STANDOUT_WORDS:
                if w in v.lower():
                    standout_f += 1
            for w in word_constants.MASCULINE_WORDS:
                if w in v.lower():
                    masculine_f += 1
            for w in word_constants.FEMININE_WORDS:
                if w in v.lower():
                    feminine_f += 1
            for w in word_constants.agentic_words:
                if w in v.lower():
                    agentic_f += 1
            for w in word_constants.communal_words:
                if w in v.lower():
                    communal_f += 1
            for w in word_constants.career_words:
                if w in v.lower():
                    career_f += 1
            for w in word_constants.family_words:
                if w in v.lower():
                    family_f += 1
            for w in word_constants.leader_words:
                if w in v.lower():
                    leader_f += 1

    for i in tqdm(range(len(rec_letters_m)), ascii=True):
        rec_letter = rec_letters_m[i].split()
        n = len(rec_letter)
        all_m += n
        for v in rec_letter:
            for w in word_constants.ABILITY_WORDS:
                if w in v.lower():
                    ability_m += 1
            for w in word_constants.STANDOUT_WORDS:
                if w in v.lower():
                    standout_m += 1
            for w in word_constants.MASCULINE_WORDS:
                if w in v.lower():
                    masculine_m += 1
            for w in word_constants.FEMININE_WORDS:
                if w in v.lower():
                    feminine_m += 1
            for w in word_constants.agentic_words:
                if w in v.lower():
                    agentic_m += 1
            for w in word_constants.communal_words:
                if w in v.lower():
                    communal_m += 1
            for w in word_constants.career_words:
                if w in v.lower():
                    career_m += 1
            for w in word_constants.family_words:
                if w in v.lower():
                    family_m += 1
            for w in word_constants.leader_words:
                if w in v.lower():
                    leader_m += 1
                
    for i in tqdm(range(len(rec_letters_nb)), ascii=True):
        rec_letter = rec_letters_nb[i].split()
        n = len(rec_letter)
        all_nb += n
        for v in rec_letter:
            for w in word_constants.ABILITY_WORDS:
                if w in v.lower():
                    ability_nb += 1
            for w in word_constants.STANDOUT_WORDS:
                if w in v.lower():
                    standout_nb += 1
            for w in word_constants.MASCULINE_WORDS:
                if w in v.lower():
                    masculine_nb += 1
            for w in word_constants.FEMININE_WORDS:
                if w in v.lower():
                    feminine_nb += 1
            for w in word_constants.agentic_words:
                if w in v.lower():
                    agentic_nb += 1
            for w in word_constants.communal_words:
                if w in v.lower():
                    communal_nb += 1
            for w in word_constants.career_words:
                if w in v.lower():
                    career_nb += 1
            for w in word_constants.family_words:
                if w in v.lower():
                    family_nb += 1
            for w in word_constants.leader_words:
                if w in v.lower():
                    leader_nb += 1

    for i in tqdm(range(len(rec_letters_p)), ascii=True):
        rec_letter = rec_letters_p[i].split()
        n = len(rec_letter)
        all_p += n
        for v in rec_letter:
            for w in word_constants.ABILITY_WORDS:
                if w in v.lower():
                    ability_p += 1
            for w in word_constants.STANDOUT_WORDS:
                if w in v.lower():
                    standout_p += 1
            for w in word_constants.MASCULINE_WORDS:
                if w in v.lower():
                    masculine_p += 1
            for w in word_constants.FEMININE_WORDS:
                if w in v.lower():
                    feminine_p += 1
            for w in word_constants.agentic_words:
                if w in v.lower():
                    agentic_p += 1
            for w in word_constants.communal_words:
                if w in v.lower():
                    communal_p += 1
            for w in word_constants.career_words:
                if w in v.lower():
                    career_p += 1
            for w in word_constants.family_words:
                if w in v.lower():
                    family_p += 1
            for w in word_constants.leader_words:
                if w in v.lower():
                    leader_p += 1

    # For normal analysis
    small_number = 0.001
    output('Total Male Letters: {}, Total Female Letters: {}, Total Non-Binary Letters: {}, Total Person Letters: {}\n'.format(len(rec_letters_m), len(rec_letters_f), len(rec_letters_nb), len(rec_letters_p)))
    output('\n Total words found in Male letters and Female letters including Odds Ratio (>1 more likely appears in Male letters):')
    output('\n ability: Male {}, Female {}, score {}'.format(ability_m, ability_f, ((ability_m + small_number) / (all_m - ability_m + small_number)) / ((ability_f + small_number) / (all_f - ability_f + small_number))))
    output('\n standout: Male {}, Female {}, score {}'.format(standout_m, standout_f, ((standout_m + small_number) / (all_m - standout_m + small_number)) / ((standout_f + small_number) / (all_f - standout_f + small_number))))
    output('\n masculine: Male {}, Female {}, score {}'.format(masculine_m, masculine_f, ((masculine_m + small_number) / (all_m - masculine_m + small_number)) / ((masculine_f + small_number) / (all_f - masculine_f + small_number))))
    output('\n feminine: Male {}, Female {}, score {}'.format(feminine_m, feminine_f, ((feminine_m + small_number) / (all_m - feminine_m + small_number)) / ((feminine_f + small_number) / (all_f - feminine_f + small_number))))
    output('\n agentic: Male {}, Female {}, score {}'.format(agentic_m, agentic_f, ((agentic_m + small_number) / (all_m - agentic_m + small_number)) / ((agentic_f + small_number) / (all_f - agentic_f + small_number))))
    output('\n communal: Male {}, Female {}, score {}'.format(communal_m, communal_f, ((communal_m + small_number) / (all_m - communal_m + small_number)) / ((communal_f + small_number) / (all_f - communal_f + small_number))))
    output('\n career: Male {}, Female {}, score {}'.format(career_m, career_f, ((career_m + small_number) / (all_m - career_m + small_number)) / ((career_f + small_number) / (all_f - career_f + small_number))))
    output('\n family: Male {}, Female {}, score {}'.format(family_m, family_f, ((family_m + small_number) / (all_m - family_m + small_number)) / ((family_f + small_number) / (all_f - family_f + small_number))))
    output('\n leadership: Male {}, Female {}, score {}\n'.format(leader_m, leader_f, ((leader_m + small_number) / (all_m - leader_m + small_number)) / ((leader_f + small_number) / (all_f - leader_f + small_number))))

    output('\n Total words found in Male, Non-Binary and Person letters including Odds Ratio (>1 more likely appears in Male letters):')
    output('\n ability: Male {}, Non-Binary {}, Person {}, M-NB score {}, M-P score {}'.format(ability_m, ability_nb, ability_p, ((ability_m + small_number) / (all_m - ability_m + small_number)) / ((ability_nb + small_number) / (all_nb - ability_nb + small_number)), ((ability_m + small_number) / (all_m - ability_m + small_number)) / ((ability_p + small_number) / (all_p - ability_p + small_number))))
    output('\n standout: Male {}, Non-Binary {}, Person {}, M-NB score {}, M-P score {}'.format(standout_m, standout_nb, standout_p, ((standout_m + small_number) / (all_m - standout_m + small_number)) / ((standout_nb + small_number) / (all_nb - standout_nb + small_number)), ((standout_m + small_number) / (all_m - standout_m + small_number)) / ((standout_p + small_number) / (all_p - standout_p + small_number))))
    output('\n masculine: Male {}, Non-Binary {}, Person {}, M-NB score {}, M-P score {}'.format(masculine_m, masculine_nb, masculine_p, ((masculine_m + small_number) / (all_m - masculine_m + small_number)) / ((masculine_nb + small_number) / (all_nb - masculine_nb + small_number)), ((masculine_m + small_number) / (all_m - masculine_m + small_number)) / ((masculine_p + small_number) / (all_p - masculine_p + small_number))))
    output('\n feminine: Male {}, Non-Binary {}, Person {}, M-NB score {}, M-P score {}'.format(feminine_m, feminine_nb, feminine_p, ((feminine_m + small_number) / (all_m - feminine_m + small_number)) / ((feminine_nb + small_number) / (all_nb - feminine_nb + small_number)), ((feminine_m + small_number) / (all_m - feminine_m + small_number)) / ((feminine_p + small_number) / (all_p - feminine_p + small_number))))
    output('\n agentic: Male {}, Non-Binary {}, Person {}, M-NB score {}, M-P score {}'.format(agentic_m, agentic_nb, agentic_p, ((agentic_m + small_number) / (all_m - agentic_m + small_number)) / ((agentic_nb + small_number) / (all_nb - agentic_nb + small_number)), ((agentic_m + small_number) / (all_m - agentic_m + small_number)) / ((agentic_p + small_number) / (all_p - agentic_p + small_number))))
    output('\n communal: Male {}, Non-Binary {}, Person {}, M-NB score {}, M-P score {}'.format(communal_m, communal_nb, communal_p, ((communal_m + small_number) / (all_m - communal_m + small_number)) / ((communal_nb + small_number) / (all_nb - communal_nb + small_number)), ((communal_m + small_number) / (all_m - communal_m + small_number)) / ((communal_p + small_number) / (all_p - communal_p + small_number))))
    output('\n career: Male {}, Non-Binary {}, Person {}, M-NB score {}, M-P score {}'.format(career_m, career_nb, career_p, ((career_m + small_number) / (all_m - career_m + small_number)) / ((career_nb + small_number) / (all_nb - career_nb + small_number)), ((career_m + small_number) / (all_m - career_m + small_number)) / ((career_p + small_number) / (all_p - career_p + small_number))))
    output('\n family: Male {}, Non-Binary {}, Person {}, M-NB score {}, M-P score {}'.format(family_m, family_nb, family_p, ((family_m + small_number) / (all_m - family_m + small_number)) / ((family_nb + small_number) / (all_nb - family_nb + small_number)), ((family_m + small_number) / (all_m - family_m + small_number)) / ((family_p + small_number) / (all_p - family_p + small_number))))
    output('\n leadership: Male {}, Non-Binary {}, Person {}, M-NB score {}, M-P score {}\n'.format(leader_m, leader_nb, leader_p, ((leader_m + small_number) / (all_m - leader_m + small_number)) / ((leader_nb + small_number) / (all_nb - leader_nb + small_number)), ((leader_m + small_number) / (all_m - leader_m + small_number)) / ((leader_p + small_number) / (all_p - leader_p + small_number))))

    output('\n Total words found in Female, Non-Binary and Person letters including Odds Ratio (>1 more likely appears in Female letters):')
    output('\n ability: Female {}, Non-Binary {}, Person {}, F-NB score {}, F-P score {}'.format(ability_f, ability_nb, ability_p, ((ability_f + small_number) / (all_f - ability_m + small_number)) / ((ability_nb + small_number) / (all_nb - ability_nb + small_number)), ((ability_f + small_number) / (all_f - ability_f + small_number)) / ((ability_p + small_number) / (all_p - ability_p + small_number))))
    output('\n standout: Female {}, Non-Binary {}, Person {}, F-NB score {}, F-P score {}'.format(standout_f, standout_nb, standout_p, ((standout_f + small_number) / (all_f - standout_m + small_number)) / ((standout_nb + small_number) / (all_nb - standout_nb + small_number)), ((standout_f + small_number) / (all_f - standout_f + small_number)) / ((standout_p + small_number) / (all_p - standout_p + small_number))))
    output('\n masculine: Female {}, Non-Binary {}, Person {}, F-NB score {}, F-P score {}'.format(masculine_f, masculine_nb, masculine_p, ((masculine_f + small_number) / (all_f - masculine_f + small_number)) / ((masculine_nb + small_number) / (all_nb - masculine_nb + small_number)), ((masculine_f + small_number) / (all_f - masculine_f + small_number)) / ((masculine_p + small_number) / (all_p - masculine_p + small_number))))
    output('\n feminine: Female {}, Non-Binary {}, Person {}, F-NB score {}, F-P score {}'.format(feminine_f, feminine_nb, feminine_p, ((feminine_f + small_number) / (all_f - feminine_f + small_number)) / ((feminine_nb + small_number) / (all_nb - feminine_nb + small_number)), ((feminine_f + small_number) / (all_f - feminine_f + small_number)) / ((feminine_p + small_number) / (all_p - feminine_p + small_number))))
    output('\n agentic: Female {}, Non-Binary {}, Person {}, F-NB score {}, F-P score {}'.format(agentic_f, agentic_nb, agentic_p, ((agentic_f + small_number) / (all_f - agentic_f + small_number)) / ((agentic_nb + small_number) / (all_nb - agentic_nb + small_number)), ((agentic_f + small_number) / (all_f - agentic_f + small_number)) / ((agentic_p + small_number) / (all_p - agentic_p + small_number))))
    output('\n communal: Female {}, Non-Binary {}, Person {}, F-NB score {}, F-P score {}'.format(communal_f, communal_nb, communal_p, ((communal_f + small_number) / (all_f - communal_f + small_number)) / ((communal_nb + small_number) / (all_nb - communal_nb + small_number)), ((communal_f + small_number) / (all_f - communal_f + small_number)) / ((communal_p + small_number) / (all_p - communal_p + small_number))))
    output('\n career: Female {}, Non-Binary {}, Person {}, F-NB score {}, F-P score {}'.format(career_f, career_nb, career_p, ((career_f + small_number) / (all_f - career_f + small_number)) / ((career_nb + small_number) / (all_nb - career_nb + small_number)), ((career_f + small_number) / (all_f - career_f + small_number)) / ((career_p + small_number) / (all_p - career_p + small_number))))
    output('\n family: Female {}, Non-Binary {}, Person {}, F-NB score {}, F-P score {}'.format(family_f, family_nb, family_p, ((family_f + small_number) / (all_f - family_f + small_number)) / ((family_nb + small_number) / (all_nb - family_nb + small_number)), ((family_f + small_number) / (all_f - family_f + small_number)) / ((family_p + small_number) / (all_p - family_p + small_number))))
    output('\n leadership: Female {}, Non-Binary {}, Person {}, F-NB score {}, F-P score {}'.format(leader_f, leader_nb, leader_p, ((leader_f + small_number) / (all_f - leader_f + small_number)) / ((leader_nb + small_number) / (all_nb - leader_nb + small_number)), ((leader_f + small_number) / (all_f - leader_f + small_number)) / ((leader_p + small_number) / (all_p - leader_p + small_number))))
    if output_file:
        output_file.close()
