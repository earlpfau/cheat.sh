import abc

class Adapter(object):

    _adapter_name = None
    _output_format = 'code'
    _cache_needed = False

    def __init__(self):
        self._list = {None: self._get_list()}

    @abc.abstractmethod
    def _get_list(self, prefix=None):
        return []

    def get_list(self, prefix=None):
        """
        Return available pages for `prefix`
        """

        if prefix in self._list:
            return self._list[prefix]

        self._list[prefix] = set(self._get_list(prefix=prefix))
        return self._list[prefix]

    def is_found(self, topic):
        """
        check if `topic` is available
        CAUTION: only root is checked
        """
        return topic in self._list[None]

    def is_cache_needed(self):
        """
        Return True if answers should be cached.
        Return False if answers should not be cached.
        """
        return self._cache_needed

    @abc.abstractmethod
    def _get_page(self, topic, request_options=None):
        """
        Return page for `topic`
        """
        pass

    def _get_output_format(self, topic):
        if '/' in topic:
            subquery = topic.split('/')[-1]
        else:
            subquery = topic

        if subquery in [':list']:
            return 'text'
        return self._output_format

    def get_page_dict(self, topic, request_options=None):
        """
        Return page dict for `topic`
        """
        answer_dict = {
            'topic': topic,
            'topic_type': self._adapter_name,
            'answer': self._get_page(topic, request_options=request_options),
            'format': self._get_output_format(topic),
            }
        return answer_dict
