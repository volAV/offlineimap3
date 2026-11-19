# SPDX-License-Identifier: GPL-2.0-or-later
"""Offline folder-sync regressions; no network, credentials, or real mail."""

import time
import unittest
from types import SimpleNamespace
from unittest import mock

from offlineimap import accounts


class Folder:
    def __init__(self, repository, messages, valid=True):
        self.repository = repository
        self.messages = dict(messages)
        self.valid = valid
        self.maxage = None
        self.startdate = None
        self.saved = False

    def getfullname(self):
        return "fixture/INBOX"

    def getname(self):
        return "INBOX"

    getvisiblename = getname

    def getmessagecount(self):
        return len(self.messages)

    def getmessageuidlist(self):
        return list(self.messages)

    def getmaxage(self):
        return self.maxage

    def getstartdate(self):
        return self.startdate

    def retrieve_min_uid(self):
        return 1

    def check_uidvalidity(self):
        return self.valid

    def save_uidvalidity(self):
        self.valid = True

    def cachemessagelist(self, **kwargs):
        pass

    def dropmessagelistcache(self):
        pass

    def openfiles(self):
        pass

    def closefiles(self):
        pass

    def syncmessagesto(self, destination, status):
        destination.messages.update(self.messages)

    def save(self):
        self.saved = True


def repository():
    return SimpleNamespace(
        restore_atime=lambda: None,
        getlocalroot=lambda: "/fixture",
        getsep=lambda: "/",
        getconfboolean=lambda name, default: False,
    )


class UIDValidityTest(unittest.TestCase):
    def setup_folders(self, mode="full", mismatch=None, empty=False):
        local_repo, remote_repo, status_repo = repository(), repository(), repository()
        self.local = Folder(local_repo, {} if empty else {11: "local message"})
        self.remote = Folder(remote_repo, {11: "local message", 22: "server-only message"})
        self.status = Folder(status_repo, {} if empty else {11: "local message"})
        if mismatch:
            getattr(self, mismatch).valid = False
        date = time.struct_time((2020, 1, 1, 0, 0, 0, 2, 1, -1))
        if mode == "maxage":
            self.local.maxage = date
        elif mode == "localstart":
            self.local.startdate = date
        elif mode == "remotestart":
            self.remote.startdate = date
        status_repo.getfolder = lambda name: self.status
        self.account = SimpleNamespace(
            name="uid-validity-fixture",
            getname=lambda: "uid-validity-fixture",
            remoterepos=remote_repo,
            localrepos=local_repo,
            statusrepos=status_repo,
            get_local_folder=lambda remote: self.local,
        )
        self.ui = mock.Mock()

    def synchronize(self):
        with mock.patch.object(accounts, "getglobalui", return_value=self.ui), \
                mock.patch.object(accounts.mbnames, "add"), \
                mock.patch.object(accounts, "SYNC_MUTEXES", {}):
            accounts.syncfolder(self.account, self.remote, quick=False)
        self.ui.error.assert_not_called()

    def test_mismatch_cannot_copy_upload_or_save_synchronization_state(self):
        for mode in ["full", "maxage", "localstart", "remotestart"]:
            for side in ["local", "remote"]:
                with self.subTest(mode=mode, side=side):
                    self.setup_folders(mode, side)
                    before_local = dict(self.local.messages)
                    before_remote = dict(self.remote.messages)
                    self.synchronize()
                    self.assertEqual(self.local.messages, before_local)
                    self.assertEqual(self.remote.messages, before_remote)
                    self.assertFalse(self.status.saved)
                    self.assertFalse(getattr(self, side).valid)

    def test_matching_validity_still_copies_new_server_messages(self):
        self.setup_folders()
        self.synchronize()
        self.assertEqual(self.local.messages[22], "server-only message")
        self.assertTrue(self.status.saved)

    def test_empty_local_folder_initializes_validity_and_downloads(self):
        self.setup_folders(mismatch="remote", empty=True)
        self.local.valid = False
        self.synchronize()
        self.assertTrue(self.local.valid)
        self.assertTrue(self.remote.valid)
        self.assertEqual(self.local.messages, self.remote.messages)
        self.assertTrue(self.status.saved)


if __name__ == "__main__":
    unittest.main()
