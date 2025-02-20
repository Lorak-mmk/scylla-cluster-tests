import logging
import random
from enum import Enum

import yaml

from sdcm.cluster import BaseNode

LOGGER = logging.getLogger(__name__)


class GcMode(Enum):
    REPAIR = "repair"
    DISABLED = "disabled"
    TIMEOUT = "timeout"
    IMMEDIATE = "immediate"


class CompactionStrategy(Enum):
    LEVELED = "LeveledCompactionStrategy"
    SIZE_TIERED = "SizeTieredCompactionStrategy"
    TIME_WINDOW = "TimeWindowCompactionStrategy"
    INCREMENTAL = "IncrementalCompactionStrategy"
    IN_MEMORY = "InMemoryCompactionStrategy"
    DATE_TIERED = "DateTieredCompactionStrategy"

    @classmethod
    def from_str(cls, output_str):
        try:
            return CompactionStrategy[CompactionStrategy(output_str).name]
        except AttributeError as attr_err:
            err_msg = "Could not recognize compaction strategy value: {} - {}".format(output_str, attr_err)
            raise ValueError(err_msg) from attr_err


def get_gc_mode(node: BaseNode, keyspace: str, table: str) -> str | GcMode:
    """Get a given table GC mode

    :Arguments:
        node
        keyspace
        table
    """
    table_gc_mode_result = node.run_cqlsh(
        f'SELECT extensions FROM system_schema.tables where keyspace_name = {keyspace} and table_name = {table}',
        split=True)
    LOGGER.debug("Query result for %s.%s GC mode is: %s", keyspace, table, table_gc_mode_result)
    gc_mode = 'N/A'
    if table_gc_mode_result and len(table_gc_mode_result) >= 4:
        extensions_value = table_gc_mode_result[3]
        # TODO: A temporary workaround until 5.0 query-table-extensions issue is fixed:
        # https://github.com/scylladb/scylla/issues/10309
        if '6d6f646506000000' in extensions_value:
            return GcMode.REPAIR
        elif '6d6f646507000000' in extensions_value:
            return GcMode.TIMEOUT
        elif '6d6f646509000000' in extensions_value:
            return GcMode.IMMEDIATE
        elif '6d6f646508000000' in extensions_value:
            return GcMode.DISABLED

    LOGGER.debug("Query result for %s.%s GC mode is: %s", keyspace, table, gc_mode)
    return gc_mode


def get_compaction_strategy(node, keyspace, table):
    """Get a given table compaction strategy

    Arguments:
        node {str} -- ip of db_node
        keyspace
        table
    """
    list_tables_compaction = node.run_cqlsh('SELECT keyspace_name, table_name, compaction FROM system_schema.tables',
                                            split=True)
    compaction = 'N/A'
    for row in list_tables_compaction:
        if '|' not in row:
            continue
        list_stripped_values = [val.strip() for val in row.split('|')]
        if list_stripped_values[0] == keyspace and list_stripped_values[1] == table:
            dict_compaction_values = yaml.safe_load(list_stripped_values[2])
            compaction = CompactionStrategy.from_str(output_str=dict_compaction_values['class'])
            break

    LOGGER.debug("Query result for {}.{} compaction is: {}".format(keyspace, table, compaction))
    return compaction


def get_compaction_random_additional_params():
    """

    :return: list_additional_params
    """
    bucket_high = round(random.uniform(1.1, 1.8), 2)
    bucket_low = round(random.uniform(0.3, 0.8), 2)
    min_sstable_size = random.randint(10, 500)
    min_threshold = random.randint(2, 10)
    max_threshold = random.randint(4, 64)
    sstable_size_in_mb = random.randint(50, 2000)
    list_additional_params = [{'bucket_high': bucket_high}, {'bucket_low': bucket_low},
                              {'min_sstable_size': min_sstable_size}, {'min_threshold': min_threshold},
                              {'max_threshold': max_threshold}, {'sstable_size_in_mb': sstable_size_in_mb}]

    return list_additional_params
