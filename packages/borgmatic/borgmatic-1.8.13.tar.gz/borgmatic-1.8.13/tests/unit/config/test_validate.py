import os
import sys
from io import StringIO

import pytest
from flexmock import flexmock

from borgmatic.config import validate as module


def test_schema_filename_finds_schema_path():
    schema_path = '/var/borgmatic/config/schema.yaml'

    flexmock(os.path).should_receive('dirname').and_return('/var/borgmatic/config')
    builtins = flexmock(sys.modules['builtins'])
    builtins.should_receive('open').with_args(schema_path).and_return(StringIO())
    assert module.schema_filename() == schema_path


def test_schema_filename_raises_filenotfounderror():
    schema_path = '/var/borgmatic/config/schema.yaml'

    flexmock(os.path).should_receive('dirname').and_return('/var/borgmatic/config')
    builtins = flexmock(sys.modules['builtins'])
    builtins.should_receive('open').with_args(schema_path).and_raise(FileNotFoundError)

    with pytest.raises(FileNotFoundError):
        module.schema_filename()


def test_format_json_error_path_element_formats_array_index():
    module.format_json_error_path_element(3) == '[3]'


def test_format_json_error_path_element_formats_property():
    module.format_json_error_path_element('foo') == '.foo'


def test_format_json_error_formats_error_including_path():
    flexmock(module).format_json_error_path_element = lambda element: f'.{element}'
    error = flexmock(message='oops', path=['foo', 'bar'])

    assert module.format_json_error(error) == "At 'foo.bar': oops"


def test_format_json_error_formats_error_without_path():
    flexmock(module).should_receive('format_json_error_path_element').never()
    error = flexmock(message='oops', path=[])

    assert module.format_json_error(error) == 'At the top level: oops'


def test_validation_error_string_contains_errors():
    flexmock(module).format_json_error = lambda error: error.message
    error = module.Validation_error('config.yaml', ('oops', 'uh oh'))

    result = str(error)

    assert 'config.yaml' in result
    assert 'oops' in result
    assert 'uh oh' in result


def test_apply_logical_validation_raises_if_unknown_repository_in_check_repositories():
    flexmock(module).format_json_error = lambda error: error.message

    with pytest.raises(module.Validation_error):
        module.apply_logical_validation(
            'config.yaml',
            {
                'repositories': ['repo.borg', 'other.borg'],
                'keep_secondly': 1000,
                'check_repositories': ['repo.borg', 'unknown.borg'],
            },
        )


def test_apply_logical_validation_does_not_raise_if_known_repository_path_in_check_repositories():
    module.apply_logical_validation(
        'config.yaml',
        {
            'repositories': [{'path': 'repo.borg'}, {'path': 'other.borg'}],
            'keep_secondly': 1000,
            'check_repositories': ['repo.borg'],
        },
    )


def test_apply_logical_validation_does_not_raise_if_known_repository_label_in_check_repositories():
    module.apply_logical_validation(
        'config.yaml',
        {
            'repositories': [
                {'path': 'repo.borg', 'label': 'my_repo'},
                {'path': 'other.borg', 'label': 'other_repo'},
            ],
            'keep_secondly': 1000,
            'check_repositories': ['my_repo'],
        },
    )


def test_apply_logical_validation_does_not_raise_if_archive_name_format_and_prefix_present():
    module.apply_logical_validation(
        'config.yaml',
        {
            'archive_name_format': '{hostname}-{now}',  # noqa: FS003
            'prefix': '{hostname}-',  # noqa: FS003
            'prefix': '{hostname}-',  # noqa: FS003
        },
    )


def test_apply_logical_validation_does_not_raise_otherwise():
    module.apply_logical_validation('config.yaml', {'keep_secondly': 1000})


def test_normalize_repository_path_passes_through_remote_repository():
    repository = 'example.org:test.borg'

    module.normalize_repository_path(repository) == repository


def test_normalize_repository_path_passes_through_file_repository():
    repository = 'file:///foo/bar/test.borg'
    flexmock(module.os.path).should_receive('abspath').and_return('/foo/bar/test.borg')

    module.normalize_repository_path(repository) == '/foo/bar/test.borg'


def test_normalize_repository_path_passes_through_absolute_repository():
    repository = '/foo/bar/test.borg'
    flexmock(module.os.path).should_receive('abspath').and_return(repository)

    module.normalize_repository_path(repository) == repository


def test_normalize_repository_path_resolves_relative_repository():
    repository = 'test.borg'
    absolute = '/foo/bar/test.borg'
    flexmock(module.os.path).should_receive('abspath').and_return(absolute)

    module.normalize_repository_path(repository) == absolute


def test_repositories_match_does_not_raise():
    flexmock(module).should_receive('normalize_repository_path')

    module.repositories_match('foo', 'bar')


def test_guard_configuration_contains_repository_does_not_raise_when_repository_in_config():
    flexmock(module).should_receive('repositories_match').replace_with(
        lambda first, second: first == second
    )

    module.guard_configuration_contains_repository(
        repository='repo', configurations={'config.yaml': {'repositories': ['repo']}}
    )


def test_guard_configuration_contains_repository_does_not_raise_when_repository_label_in_config():
    module.guard_configuration_contains_repository(
        repository='repo',
        configurations={'config.yaml': {'repositories': [{'path': 'foo/bar', 'label': 'repo'}]}},
    )


def test_guard_configuration_contains_repository_does_not_raise_when_repository_not_given():
    module.guard_configuration_contains_repository(
        repository=None, configurations={'config.yaml': {'repositories': ['repo']}}
    )


def test_guard_configuration_contains_repository_errors_when_repository_missing_from_config():
    flexmock(module).should_receive('repositories_match').replace_with(
        lambda first, second: first == second
    )

    with pytest.raises(ValueError):
        module.guard_configuration_contains_repository(
            repository='nope',
            configurations={'config.yaml': {'repositories': ['repo', 'repo2']}},
        )


def test_guard_single_repository_selected_raises_when_multiple_repositories_configured_and_none_selected():
    with pytest.raises(ValueError):
        module.guard_single_repository_selected(
            repository=None,
            configurations={'config.yaml': {'repositories': ['repo', 'repo2']}},
        )


def test_guard_single_repository_selected_does_not_raise_when_single_repository_configured_and_none_selected():
    module.guard_single_repository_selected(
        repository=None,
        configurations={'config.yaml': {'repositories': ['repo']}},
    )


def test_guard_single_repository_selected_does_not_raise_when_no_repositories_configured_and_one_selected():
    module.guard_single_repository_selected(
        repository='repo',
        configurations={'config.yaml': {'repositories': []}},
    )


def test_guard_single_repository_selected_does_not_raise_when_repositories_configured_and_one_selected():
    module.guard_single_repository_selected(
        repository='repo',
        configurations={'config.yaml': {'repositories': ['repo', 'repo2']}},
    )
