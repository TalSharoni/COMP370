import argparse
import json
import pandas as pd
import random


def get_args():
    parser = argparse.ArgumentParser(description="Extract a specified number of posts from reddit into TSV format")
    parser.add_argument("-o", "--output_file", required=True, help="output TSV file")
    parser.add_argument("json_file", help="input JSON file")
    parser.add_argument("num_posts_to_output", type=int, help="number of posts to randomly select for output")
    return parser.parse_args()


def main():
    args = get_args()

    with open(args.json_file, 'r') as f:
        data = json.load(f)

    
    posts = []
    for post in data["data"]["children"]:
        p = {"Name": post["data"]["name"], "Title": post["data"]["title"], "Coding": ""}
        posts.append(p)

    if args.num_posts_to_output >= len(posts):
        selected = posts
    else:
        selected = random.sample(posts, args.num_posts_to_output)

    df = pd.DataFrame(selected)
    df.to_csv(args.output_file, sep='\t', index=False)


if __name__ == '__main__':
    main()