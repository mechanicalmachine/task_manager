import json

from django_celery_results.backends import DatabaseBackend


class ExtendedTaskResultBackend(DatabaseBackend):
    def _store_result(
        self,
        task_id,
        result,
        status,
        traceback=None,
        request=None,
        using=None
    ):
        """Store return value and status of an executed task."""
        content_type, content_encoding, result = self.encode_content(result)

        obj = self.TaskModel._default_manager.get_task(task_id)
        res = obj.as_dict()
        meta = self.decode_content(obj, res.pop('meta', None)) or {}

        new_meta = {
            **meta,
            "children": self.current_task_children(request),
        }

        new_meta.setdefault("errors", [])
        if status in ["RETRY", "FAILURE"]:
            new_meta["errors"].append(json.loads(result))

        _, _, encoded_meta = self.encode_content(
            new_meta,
        )

        task_props = {
            'content_encoding': content_encoding,
            'content_type': content_type,
            'meta': encoded_meta,
            'result': result,
            'status': status,
            'task_id': task_id,
            'traceback': traceback,
            'using': using,
        }
        task_props.update(
            self._get_extended_properties(request, traceback)
        )

        self.TaskModel._default_manager.store_result(**task_props)
        return result
