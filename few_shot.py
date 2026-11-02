import pandas as pd
import json
import os

def sanitize_str(val):
    if not isinstance(val, str):
        return val
    # Remove lone surrogates that break PyArrow
    return val.encode('utf-8', 'ignore').decode('utf-8', 'ignore')

class FewShotPosts:
    def __init__(self, file_path=None):
        if file_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(base_dir, "data", "processed_posts.json")
        self.file_path = file_path
        self.df = None
        self.unique_tags = []
        self.load_posts(self.file_path)

    def load_posts(self, file_path):
        if not os.path.exists(file_path):
            self.df = pd.DataFrame(columns=["text", "language", "line_count", "tags", "length"])
            self.unique_tags = []
            return

        with open(file_path, encoding="utf-8", errors="replace") as f:
            posts = json.load(f)
            self.df = pd.json_normalize(posts)
            if not self.df.empty:
                # Sanitize text columns to guarantee no surrogates
                for col in self.df.columns:
                    if self.df[col].dtype == object:
                        self.df[col] = self.df[col].apply(lambda x: sanitize_str(x) if isinstance(x, str) else x)

                if 'line_count' in self.df.columns:
                    self.df['length'] = self.df['line_count'].apply(self.categorize_length)
                else:
                    self.df['length'] = "Medium"
                
                # collect unique tags safely
                all_tags = []
                for tags_item in self.df['tags'].dropna():
                    if isinstance(tags_item, list):
                        all_tags.extend([sanitize_str(t) for t in tags_item])
                    elif isinstance(tags_item, str):
                        all_tags.append(sanitize_str(tags_item))
                self.unique_tags = sorted(list(set(all_tags)))
            else:
                self.unique_tags = []

    def get_filtered_posts(self, length, language, tag):
        if self.df is None or self.df.empty:
            return []
            
        def tag_matches(post_tags):
            if isinstance(post_tags, list):
                return tag in post_tags
            return tag == post_tags

        df_filtered = self.df[
            (self.df['tags'].apply(tag_matches)) &
            (self.df['language'].str.lower() == language.lower()) &
            (self.df['length'] == length)
        ]
        
        # If strict match yields nothing, relax length restriction for better few-shot prompting
        if df_filtered.empty:
            df_filtered = self.df[
                (self.df['tags'].apply(tag_matches)) &
                (self.df['language'].str.lower() == language.lower())
            ]
            
        return df_filtered.to_dict(orient='records')

    def categorize_length(self, line_count):
        if line_count < 5:
            return "Short"
        elif 5 <= line_count <= 10:
            return "Medium"
        else:
            return "Long"

    def get_tags(self):
        return self.unique_tags

    def add_custom_post(self, text, language, tags):
        """Allows users or students to expand the dataset dynamically."""
        text = sanitize_str(text)
        line_count = len([line for line in text.split("\n") if line.strip()])
        new_post = {
            "text": text,
            "language": language,
            "line_count": line_count,
            "tags": [sanitize_str(t) for t in tags] if isinstance(tags, list) else [sanitize_str(tags)]
        }
        
        data = []
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding="utf-8", errors="replace") as f:
                try:
                    data = json.load(f)
                except Exception:
                    data = []
        data.append(new_post)
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        
        self.load_posts(self.file_path)
        return True
