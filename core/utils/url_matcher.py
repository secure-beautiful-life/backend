class UrlMatcher:
    @staticmethod
    def match(pattern: str, url: str) -> bool:
        pattern_list = pattern.split("/")
        url_list = url.split("/")

        if "**" in pattern:
            pattern_list = pattern_list[:-1]
            url_list = url_list[:len(pattern_list)]

        if "*" in pattern:
            star_index_list = []
            for idx, c in enumerate(pattern_list):
                if c == "*":
                    star_index_list.append(idx)

            for idx in star_index_list:
                if (len(url_list) - 1) < idx:
                    return False

                url_list[idx] = "*"

        return pattern_list == url_list
