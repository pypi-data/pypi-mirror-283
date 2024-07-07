import builtins
import unittest

from unittest.mock import mock_open, patch, sentinel

from sapphire.corsika import qsub_store_corsika_data


class SeedsTest(unittest.TestCase):
    @patch.object(qsub_store_corsika_data.glob, 'glob')
    def test_all_seeds(self, mock_glob):
        mock_glob.return_value = ['/data/123_456', '/data/234_567']
        seeds = qsub_store_corsika_data.all_seeds()
        self.assertEqual(seeds, {'123_456', '234_567'})
        mock_glob.assert_called_once_with(qsub_store_corsika_data.DATADIR + '/*_*')

    @patch.object(qsub_store_corsika_data.glob, 'glob')
    def test_seeds_processed(self, mock_glob):
        mock_glob.return_value = ['/data/123_456/corsika.h5', '/data/234_567/corsika.h5']
        seeds = qsub_store_corsika_data.seeds_processed()
        self.assertEqual(seeds, {'123_456', '234_567'})
        mock_glob.assert_called_once_with(qsub_store_corsika_data.DATADIR + '/*_*/corsika.h5')

    def test_seeds_in_queue(self):
        with patch.object(builtins, 'open', mock_open(read_data='123_456\n234_567')) as mock_file:
            seeds = qsub_store_corsika_data.seeds_in_queue()
        mock_file.assert_called_once_with(qsub_store_corsika_data.QUEUED_SEEDS)
        self.assertEqual(seeds, {'123_456', '234_567'})
        self.assertTrue(mock_file().read.called)

        # Empty set if log not available
        with patch.object(builtins, 'open', mock_open()) as mock_file:
            mock_file.side_effect = OSError('no log!')
            seeds = qsub_store_corsika_data.seeds_in_queue()
        mock_file.assert_called_with(qsub_store_corsika_data.QUEUED_SEEDS)
        self.assertEqual(seeds, set())

    def test_write_queued_seeds(self):
        mock_file = mock_open()
        seeds = {'123_456', '234_567'}
        with patch.object(builtins, 'open', mock_file):
            qsub_store_corsika_data.write_queued_seeds(seeds)
        mock_file.assert_called_once_with(qsub_store_corsika_data.QUEUED_SEEDS, 'w')
        mock_file().write.assert_called_once_with('\n'.join(seeds))

    @patch.object(qsub_store_corsika_data, 'seeds_in_queue')
    @patch.object(qsub_store_corsika_data, 'write_queued_seeds')
    def test_append_queued_seeds(self, mock_write_seeds, mock_seeds_in_queue):
        mock_seeds_in_queue.return_value = {sentinel.seed1, sentinel.seed2}
        qsub_store_corsika_data.append_queued_seeds({sentinel.seed3})
        mock_write_seeds.assert_called_once_with({sentinel.seed1, sentinel.seed2, sentinel.seed3})

    @patch.object(qsub_store_corsika_data, 'all_seeds')
    @patch.object(qsub_store_corsika_data, 'seeds_processed')
    @patch.object(qsub_store_corsika_data, 'seeds_in_queue')
    @patch.object(qsub_store_corsika_data, 'write_queued_seeds')
    def test_get_seeds_todo(self, mock_write, mock_queued, mock_processed, mock_all):
        mock_queued.return_value = {sentinel.queued, sentinel.processed}
        mock_processed.return_value = {sentinel.processed}
        mock_all.return_value = {sentinel.queued, sentinel.processed, sentinel.unprocessed}
        seeds = qsub_store_corsika_data.get_seeds_todo()
        mock_write.assert_called_once_with({sentinel.queued})
        self.assertEqual(seeds, {sentinel.unprocessed})

    def test_store_command(self):
        tmp = qsub_store_corsika_data.DATADIR
        qsub_store_corsika_data.DATADIR = '/data'
        command = qsub_store_corsika_data.store_command('123_456')
        self.assertEqual(
            command,
            '/data/hisparc/env/miniconda/envs/corsika/bin/python '
            '/data/hisparc/env/miniconda/envs/corsika/bin/store_corsika_data '
            '/data/123_456/DAT000000 /data/123_456/corsika.h5',
        )
        qsub_store_corsika_data.DATADIR = tmp

    @patch.object(qsub_store_corsika_data.os.path, 'getsize')
    @patch.object(qsub_store_corsika_data.os, 'umask')
    @patch.object(qsub_store_corsika_data, 'get_seeds_todo')
    @patch.object(qsub_store_corsika_data.qsub, 'check_queue')
    @patch.object(qsub_store_corsika_data, 'store_command')
    @patch.object(qsub_store_corsika_data.qsub, 'submit_job')
    @patch.object(qsub_store_corsika_data, 'append_queued_seeds')
    @patch.object(qsub_store_corsika_data, 'SCRIPT_TEMPLATE')
    def test_run(
        self,
        mock_template,
        mock_append,
        mock_submit,
        mock_store,
        mock_check,
        mock_get_seeds,
        mock_umask,
        mock_size,
    ):
        seeds = {'123_456', '234_567'}
        mock_size.return_value = 12355
        mock_get_seeds.return_value = seeds.copy()
        mock_check.return_value = 6
        mock_template.format.return_value = sentinel.script
        mock_store.return_value = sentinel.command
        qsub_store_corsika_data.run(sentinel.queue)
        for seed in seeds:
            mock_submit.assert_any_call(sentinel.script, seed, sentinel.queue, '')
            mock_append.assert_any_call([seed])
        mock_template.format.assert_called_with(command=sentinel.command, datadir=qsub_store_corsika_data.DATADIR)
        mock_umask.assert_called_once_with(0o02)
