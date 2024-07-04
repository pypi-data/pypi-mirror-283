import logging

from ios_device.remote.remote_lockdown import RemoteLockdownClient
from ios_device.util.lockdown import LockdownClient

notifications = ['com.apple.security.secureobjectsync.viewschanged', 'com.apple.AOSNotification.FMIPStateDidChange',
                 'com.apple.assistant.siri_settings_did_change', 'CNFavoritesChangedExternallyNotification',
                 'com.apple.security.view-change.PCS', 'com.apple.ap.adprivacyd.reconcile',
                 'com.apple.duetexpertd.ATXAnchorModel.WiredAudioDeviceConnectedAnchor',
                 'com.apple.ams.privateListeningChanged',
                 'com.apple.rapport.prefsChanged', 'com.apple.locationd.authorization',
                 'com.apple.cmfsyncagent.storedidchangeexternally',
                 'com.apple.homed.user-cloud-share.wake.com.apple.siri.zonesharing',
                 'com.apple.ProtectedCloudStorage.mobileBackupStateChange',
                 'com.apple.MobileAsset.CoreTextAssets.ma.new-asset-installed',
                 'com.apple.coreduet.idslaunchnotification',
                 'com.apple.accessibility.cache.enhance.text.legibility', 'com.apple.system.config.network_change',
                 'com.apple.MobileAsset.VoiceTriggerAssetsIPad.ma.new-asset-installed',
                 'com.apple.LaunchServices.applicationUnregistered',
                 'com.apple.coreduetd.knowledgebase.launch.duetexpertd',
                 'com.apple.homed.user-cloud-share.repair.wake.com.apple.applemediaservices.multiuser',
                 'com.apple.tv.appRemoved',
                 'com.apple.MobileSoftwareUpdate.OSVersionChanged', 'AppleNumberPreferencesChangedNotification',
                 'com.apple.isp.frontcamerapower', 'HKHealthDaemonActiveWorkoutServersDidUpdateNotification',
                 'com.apple.networkserviceproxy.reset', 'com.apple.appstored.PodcastSubEntitlementsCacheUpdated',
                 'com.apple.homed.televisionAccessoryAdded', 'com.apple.sbd.kvstorechange',
                 'com.apple.MobileAsset.VoiceTriggerAssetsWatch.ma.new-asset-installed',
                 'com.apple.ContinuityKeyBoard.enabled',
                 'CKIdentityUpdateNotification', 'com.apple.assistant.speech-capture.finished',
                 'com.apple.proactive.PersonalizationPortrait.namedEntitiesDidChangeMeaningfully',
                 '__ABDataBaseChangedByOtherProcessNotification', 'com.apple.navd.wakeUpForHypothesisUpdate',
                 'com.apple.language.changed', 'com.apple.family.family_updated',
                 'com.apple.duetexpertd.mm.audiodisconnect',
                 'com.apple.itunesstored.accountschanged', 'com.apple.EscrowSecurityAlert.record',
                 'com.apple.AirTunes.DACP.play',
                 'com.apple.alarm.label.siri_data_changed', 'com.apple.UsageTrackingAgent.registration.video',
                 'com.apple.StoreServices.StorefrontChanged',
                 'com.apple.accessibility.cache.darken.system.colors.enabled',
                 'com.apple.trial.NamespaceUpdate.SIRI_UNDERSTANDING_ASR_ASSISTANT',
                 'com.apple.VideoSubscriberAccount.DidRegisterSubscription', 'com.apple.system.clock_set',
                 'com.apple.media.podcasts.siri_data_changed', 'com.apple.networkextension.apps-changed',
                 'kAFPreferencesDidChangeDarwinNotification', 'com.apple.callhistory.RecentsClearedNotification',
                 'MISProvisioningProfileRemoved', 'com.apple.springboard.finishedstartup',
                 'com.apple.welcomemat.finalizeMigratableApps', 'com.apple.coreaudio.borealisTrigger',
                 'com.apple.MobileAsset.VoiceTriggerAssetsWatch.new-asset-installed',
                 'com.apple.cddcommunicator.pluginChanged',
                 'com.apple.security.view-change.SE-PTC', 'com.apple.voicetrigger.enablePolicyChanged',
                 'com.apple.CloudSubscriptionFeature.Changed', 'com.apple.security.cloudkeychainproxy.kvstorechange3',
                 'com.apple.AirTunes.DACP.devicevolume', 'com.apple.homed.AppleTVAccessoryAdded',
                 'kKeepAppsUpToDateEnabledChangedNotification', 'com.apple.security.octagon.trust-status-change',
                 'com.apple.siri.inference.biome-context', 'com.apple.tv.updateAppVisibility',
                 'com.apple.sockpuppet.applications.updated',
                 'com.apple.softwareupdateservicesd.SUCoreConfigScheduledScan',
                 'com.apple.MobileAsset.CoreTextAssets.ma.cached-metadata-updated',
                 'com.apple.ap.adprivacyd.iTunesActiveStorefrontDidChangeNotification',
                 'com.apple.appstored.AppStoreSubEntitlementsCacheUpdated',
                 'com.apple.remotemanagement.accountsChanged',
                 'com.apple.coreduet.client-needs-help.coreduetd', 'com.apple.LaunchServices.ApplicationsChanged',
                 'com.apple.navd.backgroundCommute.startPredicting', 'com.apple.suggestions.prepareForQuery',
                 'com.apple.LaunchServices.applicationRegistered', 'com.apple.icloud.fmip.siri_data_changed',
                 'com.apple.carkit.carplay-attached', 'com.apple.photostream.idslaunchnotification',
                 'com.apple.voicemail.ReloadService', 'com.apple.homed.speakersConfiguredChanged',
                 'com.apple.duetexpertd.ATXMMAppPredictor.WiredAudioDeviceDisconnectedAnchor',
                 'com.apple.icloud.fmip.lostmode.enable',
                 'com.apple.pasteboard.notify.changed', 'com.apple.icloudpairing.idslaunchnotification',
                 'com.apple.remindd.nano_preferences_sync', 'kVMVoicemailTranscriptionTaskTranscribeAllVoicemails',
                 'com.apple.bluetooth.daemonStarted', 'com.apple.security.view-ready.SE-PTC',
                 'com.apple.system.logging.power_button_notification',
                 'com.apple.MobileAsset.VoiceTriggerAssetsMarsh.ma.new-asset-installed',
                 'com.apple.MobileBackup.backgroundCellularAccessChanged', 'com.apple.nanoregistry.devicedidunpair',
                 'com.apple.awd.launch.wifi', 'com.apple.OTACrashCopier.SubmissionPreferenceChanged',
                 'com.apple.aggregated.addaily.logging', 'com.apple.atc.xpc.runkeeplocaltask',
                 'com.apple.springboard.hasBlankedScreen',
                 'com.apple.MobileAsset.TimeZoneUpdate.ma.cached-metadata-updated',
                 'com.apple.security.publickeynotavailable',
                 'com.apple.shortcuts.daemon-wakeup-request', 'com.apple.cmfsyncagent.kvstorechange',
                 'com.apple.dmd.iCloudAccount.didChange',
                 'com.apple.trial.NamespaceUpdate.SIRI_VALUE_INFERENCE_CONTACT_RESOLUTION',
                 'kCalBirthdayDefaultAlarmChangedNote', 'com.apple.voicetrigger.PHSProfileModified',
                 'com.apple.UsageTrackingAgent.registration.application', 'FMFMeDeviceChangedNotification',
                 'com.apple.mobilecal.preference.notification.weekStart',
                 'com.apple.duetexpertd.ATXMMAppPredictor.BluetoothDisconnectedAnchor',
                 'com.apple.softwareupdateservicesd.activity.autoScan', 'com.apple.siri.preheat.quiet',
                 'com.apple.voicemail.VVVerifierCheckpointDictionaryChanged',
                 'com.apple.SafariShared.Assistant.reload_plugin',
                 'com.apple.reminder.list.name.siri_data_changed', 'com.apple.purplebuddy.setupexited',
                 'com.apple.calendar.database.preference.notification.kCalPreferredDaysToSyncKey',
                 'com.apple.softwareupdateservicesd.activity.autoDownloadEnd',
                 'com.apple.system.batterysavermode.auto_disabled',
                 'com.apple.security.secureobjectsync.circlechanged', 'NewOperatorNotification',
                 'com.apple.spotlight.SyndicatedContentDeleted',
                 'com.apple.MobileAsset.ProactiveEventTrackerAssets.ma.cached-metadata-updated',
                 'com.apple.appstored.ActivitySubEntitlementsCacheUpdated', 'com.apple.suggestions.settingsChanged',
                 'com.apple.voicetrigger.RemoteDarwin.ConnectionChanged',
                 'com.apple.icloud.findmydeviced.findkit.magSafe.added',
                 'com.apple.locationd.appreset',
                 'com.apple.MobileAsset.VoiceServicesVocalizerVoice.ma.cached-metadata-updated',
                 'com.apple.assistant.sync_needed', 'com.apple.pushproxy.idslaunchnotification',
                 'com.apple.nfcacd.multitag.state.change',
                 'com.apple.MobileAsset.SecureElementServiceAssets.ma.cached-metadata-updated',
                 'com.apple.duetexpertd.mm.bluetoothdisconnect', 'com.apple.system.batterysavermode.first_time',
                 'com.apple.touchsetupd.launch', 'com.apple.homehubd.endpointDeactivated',
                 'NoteContextDarwinNotificationWithLoggedChanges', 'com.apple.mobileipod.librarychanged',
                 'com.apple.UsageTrackingAgent.registration.web-domain', 'com.apple.siri.cloud.synch.changed',
                 'com.apple.proactive.queries.databaseChange', 'com.apple.smartcharging.defaultschanged',
                 'com.apple.screensharing.idslaunchnotification', 'FMFDevicesChangedNotification',
                 'com.apple.GeoServices.countryCodeChanged', 'com.apple.powerui.smartcharge',
                 'com.apple.MobileAsset.VoiceServices.GryphonVoice.ma.new-asset-installed',
                 'com.apple.assistant.sync_homekit_now',
                 'com.apple.icloud.findmydeviced.findkit.magSafe.attach',
                 'com.apple.icloud.searchparty.accessoryDidPair',
                 'com.apple.SensorKit.als', 'com.apple.voicetrigger.RemoteDarwin.EarlyDetect',
                 'com.apple.telephonyutilities.callservicesd.fakeincomingmessage',
                 'com.apple.nanoregistry.paireddevicedidchangecapabilities',
                 'com.apple.voiceservices.notification.voice-update',
                 'com.apple.duetbm.internalSettingsChanged',
                 'com.apple.nanophotos.prefs.LibraryCollectionTargetMapData-changed',
                 'com.apple.pex.connections.focalappchanged',
                 'com.apple.accessibility.cache.enhance.background.contrast',
                 'com.apple.MobileAsset.VoiceServices.VoiceResources.ma.new-asset-installed',
                 'com.apple.idscredentials.idslaunchnotification',
                 'com.apple.accessories.connection.MFi4AccessoryDisconnected',
                 'com.apple.mobileme.fmf1.allowFindMyFriendsModification',
                 'com.apple.MobileAsset.TimeZoneUpdate.ma.new-asset-installed',
                 'com.apple.homed.user-cloud-share.wake.com.apple.mediaservicesbroker.container',
                 'com.apple.contacts.clientDidDisplayFavorites', 'com.apple.bluetooth.WirelessSplitterOn',
                 'com.apple.mobileipod.displayvalueschanged', 'com.apple.coremedia.carplayisconnected',
                 'com.apple.duetexpertd.donationmonitor.intent', 'com.apple.mobiletimerd.wakeuptest',
                 'com.apple.powermanagement.systempowerstate', 'com.apple.AppleMediaServices.deviceOffersChanged',
                 'com.apple.AirTunes.DACP.shuffletoggle', 'com.apple.AirTunes.DACP.previtem',
                 'com.apple.powermanagement.restartpreventers', 'com.apple.SensorKit.phoneUsageReport',
                 'com.apple.awd.launch.nfcd',
                 'com.apple.private.SensorKit.pedometer.stridecalibration', 'com.apple.mobile.disk_image_mounted',
                 'com.apple.ManagedConfiguration.webContentFilterTypeChanged',
                 'com.apple.ProximityControl.LockScreenDiscovery',
                 'com.apple.awdd.anonymity', 'com.apple.sleep.sync.SleepScheduleDidChange',
                 'com.apple.mobileipod.keeplocalstatechanged', 'com.apple.assistant.sync_data_changed',
                 'com.apple.locationd.vehicle.exit', 'com.apple.carkit.capabilities-changed',
                 'com.apple.parsecd.queries.clearData',
                 'com.apple.parsecd.bag', 'com.apple.MobileAsset.VoiceTriggerAssetsMarsh.ma.cached-metadata-updated',
                 'com.apple.duetexpertd.dockAppListCacheUpdate', 'com.apple.itunesstored.autodownloaddefaultschange',
                 'com.apple.powerlog.batteryServiceNotification', 'AppleLanguagePreferencesChangedNotification',
                 'com.apple.voiceservices.trigger.asset-force-update', 'com.apple.itunesstored.invalidatebags',
                 'com.apple.duetexpertd.defaultsChanged', 'com.apple.security.itembackup',
                 'com.apple.powermanagement.idlesleeppreventers', 'com.apple.system.batterysavermode',
                 'SBApplicationNotificationStateChanged', 'com.apple.proactive.queries.clearData',
                 'com.apple.coreduetd.nearbydeviceschanged', 'com.apple.trial.NamespaceUpdate.FREEZER_POLICIES',
                 'com.apple.duetexpertd.ATXMMAppPredictor.CarPlayDisconnectedAnchor',
                 'com.apple.EscrowSecurityAlert.server',
                 'com.apple.siri.cloud.storage.deleted', 'com.apple.thermalmonitor.ageAwareMitigationsEnabled',
                 'com.apple.corespotlight.developer.ReindexAllItemsWithIdentifiers',
                 'com.apple.system.powersources.percent',
                 'com.apple.MusicLibrary.importFinished-/var/mobile/Media/iTunes_Control/iTunes/MediaLibrary.sqlitedb',
                 'com.apple.ProtectedCloudStorage.rollNow', 'com.apple.mobile.lockdown.device_name_changed',
                 'com.apple.mobilecal.timezonechanged', 'com.apple.mobileslideshow.ICPLStateChanged',
                 'com.apple.MobileAsset.VoiceTriggerAssets.cached-metadata-updated', 'com.apple.springboard.lockstate',
                 'com.apple.MobileAsset.SpeechEndpointAssets.ma.cached-metadata-updated',
                 'SignificantTimeChangeNotification',
                 'com.apple.trial.NamespaceUpdate.SIRI_DICTATION_ASSETS', 'com.apple.security.tick',
                 'VVMessageWaitingFallbackNotification', 'com.apple.ProtectedCloudStorage.rollIfAged',
                 'MISProvisioningProfileInstalled', 'com.apple.coreduetd.remoteDeviceChange',
                 'kFZACAppBundleIdentifierLaunchNotification',
                 'com.apple.datamigrator.datamigrationcompletecontinuerestore',
                 'com.apple.fairplayd.resync-fpkeybag', 'com.apple.mobiletimerd.resttest',
                 'com.apple.MobileAsset.VoiceTriggerAssets.ma.cached-metadata-updated',
                 'com.apple.idsremoteurlconnection.idslaunchnotification', 'com.apple.homehubd.endpointActivated',
                 'com.apple.locationd.vehicle.connected',
                 'com.apple.MobileAsset.SpeechEndpointAssets.cached-metadata-updated',
                 'com.apple.dataaccess.ping', 'com.apple.GeoServices.navigation.stopped',
                 'com.apple.softwareupdateservicesd.activity.emergencyAutoScan',
                 'com.apple.idstransfers.idslaunchnotification',
                 'com.apple.softwareupdateservicesd.activity.autoInstallUnlock',
                 'AFLanguageCodeDidChangeDarwinNotification',
                 'RTLocationsOfInterestDidChangeNotification', 'com.apple.mobiletimerd.chargetest',
                 'com.apple.VideosUI.StoreAcquisitionCrossProcessNotification',
                 'com.apple.system.powermanagement.useractivity2',
                 'com.apple.duetexpertd.ATXAnchorModel.invalidate.BluetoothConnectedAnchor',
                 'com.apple.duetexpertd.clientModelRefreshBlendingLayer', 'com.apple.chatkit.groups.siri_data_changed',
                 'com.apple.corespotlight.developer.ReindexAllItems', 'kFZVCAppBundleIdentifierLaunchNotification',
                 'AppleDatePreferencesChangedNotification', 'INVoocabularyChangedNotification',
                 'com.apple.telephonyutilities.callservicesdaemon.voicemailcallended',
                 'com.apple.MediaRemote.nowPlayingActivePlayersIsPlayingDidChange',
                 'com.apple.nanoregistry.watchdidbecomeactive',
                 'com.apple.exchangesyncd.ping', 'com.apple.networkextension.app-paths-changed',
                 'com.apple.nearfield.handoff.terminal',
                 'com.apple.cloudd.pcsIdentityUpdate-com.apple.ProactivePredictionsBackup',
                 'com.apple.cloudrecents.kvstorechange',
                 'com.apple.mobileipod.libraryimportdidfinish', 'com.apple.mobiletimerd.reset',
                 'com.apple.duetexpertd.homeScreenPageConfigCacheUpdate', 'com.apple.da.tasking_changed',
                 'com.apple.LoginKit.isLoggedIn', 'com.apple.duetexpertd.ATXAnchorModel.invalidate.IdleTimeEndAnchor',
                 'com.apple.security.cloudkeychain.forceupdate', '_CalDatabaseChangedNotification',
                 'AppleKeyboardsPreferencesChangedNotification',
                 'com.apple.UsageTrackingAgent.registration.now-playing', 'com.apple.cddcommunicator.batteryChanged',
                 'SLSharedWithYouSettingHasChanged', 'com.apple.pairedsync.syncDidComplete',
                 'com.apple.powerui.requiredFullCharge',
                 'CKAccountChangedNotification',
                 'com.apple.duetexpertd.ATXMMAppPredictor.WiredAudioDeviceConnectedAnchor',
                 'com.apple.duetexpertd.ATXAnchorModel.BluetoothConnectedAnchor',
                 'com.apple.hangtracerd.htse_state_changed',
                 'com.apple.AirTunes.DACP.repeatadv', 'com.apple.GeoServices.navigation.started',
                 'com.apple.spotlightui.prefschanged',
                 'com.apple.MobileAsset.VoiceServices.VoiceResources.new-asset-installed', 'logging tasks have changed',
                 'EKNotificationCountChangedExternallyNotification', 'com.apple.duetexpertd.donationmonitor.activity',
                 'com.apple.ProtectedCloudStorage.updatedKeys',
                 'com.apple.softwareupdateservicesd.activity.presentBanner',
                 'com.apple.ProtectedCloudStorage.rollBackupDisabled',
                 'com.apple.appstored.iCloudSubEntitlementsCacheUpdated',
                 'com.apple.stockholm.se.mfd', 'com.apple.mobiletimerd.diagnostics',
                 'com.apple.mobile.keybagd.first_unlock',
                 'com.apple.proactive.information.source.weather', 'com.apple.icloud.searchparty.selfbeaconchanged',
                 'com.apple.accessibility.cache.reduce.motion', 'com.apple.locationd.vehicular.changed.toVehicular',
                 'com.apple.bluetooth.accessory-authentication.success', 'com.apple.locationd/Prefs',
                 'com.apple.spotlight.SyndicatedContentRefreshed', 'com.apple.networkextension.nehelper-init',
                 'com.apple.managedconfiguration.allowpasscodemodificationchanged',
                 'com.apple.DuetHeuristic-BM.shutdowsoon',
                 'com.apple.system.powersources.source', 'com.apple.managedconfiguration.effectivesettingschanged',
                 'com.apple.datamigrator.migrationDidFinish', 'com.apple.nanomusic.sync.defaults',
                 'com.apple.homed.multi-user-status-changed',
                 'com.apple.siri.ShortcutsCloudKitAccountModifiedNotification',
                 'com.apple.mobilemail.afc.poll', 'com.apple.appstored.TVSubEntitlementsCacheUpdated',
                 'com.apple.duetexpertd.ATXAnchorModel.invalidate.ChargerConnectedAnchor',
                 'com.apple.ManagedConfiguration.profileListChanged', 'com.apple.duetexpertd.ms.nowplayingpause',
                 'com.apple.devicemanagementclient.longLivedTokenChanged',
                 'com.apple.MCX._managementStatusChangedForDomains',
                 'com.apple.triald.new-experiment', 'com.apple.security.secureobjectsync.holdlock',
                 'CNContactStoreDidChangeNotification', 'kFaceTimeChangedNotification',
                 'com.apple.nanoregistry.devicedidpair',
                 'com.apple.wirelessproximity.launch', 'com.apple.wcd.wake-up',
                 'com.apple.icloud.findmydeviced.localActivationLockInfoChanged', 'FMFDataUpdateCompleteNotification',
                 'com.apple.softwareupdateservicesd.activity.autoInstallEnd', 'com.apple.security.publickeyavailable',
                 'MFNanoMailImportantBridgeSettingHasChangedDarwinNotification',
                 'com.apple.duetexpertd.ms.carplaydisconnect',
                 'com.apple.MobileAsset.SecureElementServiceAssets.ma.new-asset-installed',
                 'com.apple.symptoms.materialLinkQualityChange', 'com.apple.ams.provision-biometrics',
                 'com.apple.ap.adprivacyd.canceltasks', 'com.apple.AirTunes.DACP.pause', 'com.apple.audio.AOP.enable',
                 'CalSyncClientBeginningMultiSave', 'com.apple.system.powersources.timeremaining',
                 'com.apple.mobiletimerd.bedtimetest',
                 'com.apple.tv.TVWidgetExtension.Register', 'com.apple.SensorKit.deviceUsageReport',
                 'com.apple.mobileipod-prefsChanged', 'com.apple.purplebuddy.setupdone', 'NewCarrierNotification',
                 'com.apple.bluetooth.pairing', 'com.apple.healthlite.SleepDetectedActivity',
                 'com.apple.mobilecal.invitationalertschanged', 'CalSyncClientFinishedMultiSave',
                 'com.apple.parsec-fbf.FLUploadImmediately',
                 'com.apple.MobileAsset.AppleKeyServicesCRL.new-asset-installed',
                 'com.apple.locationd.vehicle.disconnected', 'com.apple.sleepd.diagnostics',
                 'com.apple.media.entities.siri_data_changed', 'com.apple.appstored.MusicSubEntitlementsCacheUpdated',
                 'com.apple.MobileAsset.ProactiveEventTrackerAssets.ma.new-asset-installed',
                 'com.apple.icloud.findmydeviced.findkit.magSafe.detach', 'com.apple.AirTunes.DACP.volumeup',
                 'com.apple.siri.ShortcutsCloudKitAccountAddedNotification', 'com.apple.tcc.access.changed',
                 'com.apple.Music-AllowsCellularDataDownloads', 'com.apple.videos.migrationCompleted',
                 'com.apple.assistant.app_vocabulary', 'com.apple.SensorKit.visits',
                 'com.apple.managedconfiguration.passcodechanged',
                 'com.apple.icloud.FindMy.addMagSafeAccessory', 'com.apple.duetexpertd.appchangeprediction',
                 'com.apple.telephonyutilities.callservicesd.fakeoutgoingmessage',
                 'com.apple.MediaRemote.nowPlayingApplicationIsPlayingDidChange',
                 'com.apple.duetexpertd.ATXAnchorModel.ChargerConnectedAnchor',
                 'kCalEventOccurrenceCacheChangedNotification',
                 'com.apple.TVRemoteCore.connectionRequested', 'com.apple.homekit.sync-data-cache-updated',
                 'com.apple.duetexpertd.mm.bluetoothconnected', 'com.apple.mobiletimerd.waketest',
                 'com.apple.ap.adprivacyd.launch',
                 'com.apple.system.lowpowermode.auto_disabled', 'com.apple.ap.adprivacyd.deviceKnowledge',
                 'com.apple.duetexpertd.ATXMMAppPredictor.BluetoothConnectedAnchor',
                 'com.apple.system.powermanagement.poweradapter',
                 'com.apple.MobileAsset.VoiceTriggerAssets.new-asset-installed',
                 'com.apple.accessibility.cache.invert.colors',
                 'com.apple.healthlite.SleepSessionEndRequest', 'com.apple.geoservices.siri_data_changed',
                 'com.apple.appletv.backgroundstate', 'MPStoreClientTokenDidChangeNotification',
                 'com.apple.SensorKit.messagesUsageReport', 'com.apple.imautomatichistorydeletionagent.prefchange',
                 'com.apple.homed.user-cloud-share.wake.com.apple.siri.data', 'com.apple.dmd.budget.didChange',
                 'com.apple.NanoPhotos.Library.changed',
                 'com.apple.duetexpertd.ATXAnchorModel.invalidate.WiredAudioDeviceConnectedAnchor',
                 'com.apple.assistant.sync_homekit_urgent',
                 'com.apple.calendar.database.preference.notification.suggestEventLocations',
                 'com.apple.accessibility.cache.differentiate.without.color', 'EKFeatureSetDidChangeNotification',
                 'PCPreferencesDidChangeNotification',
                 'com.apple.duetexpertd.ATXAnchorModel.invalidate.CarPlayConnectedAnchor',
                 'com.apple.MobileAsset.VoiceTriggerAssetsWatch.ma.cached-metadata-updated',
                 'com.apple.rapport.CompanionLinkDeviceAdded', 'com.apple.cddcommunicator.nwchanged',
                 'com.apple.duetexpertd.ATXMMAppPredictor.CarPlayConnectedAnchor',
                 'com.apple.system.powersources.criticallevel',
                 'com.apple.BiometricKit.passcodeGracePeriodChanged', 'com.apple.powermanagement.systemsleeppreventers',
                 'SLSharedWithYouAppSettingHasChanged', 'com.apple.ManagedConfiguration.webContentFilterChanged',
                 'com.apple.duetexpertd.updateDefaultsDueToRelevantHomeScreenConfigUpdate',
                 'FMFFollowersChangedNotification',
                 'com.apple.softwareupdateservicesd.activity.installAlert',
                 'ConnectedGymPreferencesChangedNotification',
                 'com.apple.voicetrigger.XPCRestarted', 'com.apple.softwareupdateservicesd.activity.delayEndScan',
                 'com.apple.duetexpertd.ATXScreenUnlockUpdateSource',
                 'com.apple.appstored.NewsSubEntitlementsCacheUpdated',
                 'com.apple.fitness.FitnessAppInstalled', 'com.apple.managedconfiguration.restrictionchanged',
                 'com.apple.nanoregistry.paireddevicedidchangeversion', 'com.apple.iokit.hid.displayStatus',
                 'com.apple.coreaudio.RoutingConfiguration', 'com.apple.mobileipod.noncontentspropertieschanged',
                 'com.apple.GeoServices.PreferencesSync.SettingsChanged', 'com.apple.isp.backcamerapower',
                 'com.apple.duetexpertd.ATXAnchorModel.CarPlayConnectedAnchor',
                 'BYSetupAssistantFinishedDarwinNotification',
                 'com.apple.springboard.pluggedin', 'com.apple.AirTunes.DACP.device-prevent-playback',
                 'com.apple.duetexpertd.ms.carplayconnect', 'com.apple.accessories.connection.passedMFi4Auth',
                 'CNContactStoreMeContactDidChangeNotification', 'com.apple.MediaRemote.nowPlayingInfoDidChange',
                 'com.apple.system.thermalpressurelevel', 'com.apple.mobile.lockdown.activation_state',
                 'com.apple.homed.user-cloud-share.wake.com.apple.applemediaservices.multiuser.qa',
                 'com.apple.AirTunes.DACP.devicevolumechanged', 'com.apple.system.hostname',
                 'com.apple.system.lowpowermode.first_time',
                 'com.apple.mobileslideshow.PLNotificationKeepOriginalsChanged',
                 'com.apple.mobilecal.preference.notification.calendarsExcludedFromNotifications',
                 'com.apple.MobileAsset.VoiceTriggerAssetsIPad.ma.cached-metadata-updated',
                 'com.apple.duetexpertd.feedbackavailable',
                 'com.apple.MobileAsset.VoiceTriggerAssets.ma.new-asset-installed',
                 'com.apple.duetexpertd.ms.nowplayingplay',
                 'com.apple.CallHistoryPluginHelper.launchnotification', 'com.apple.cddcommunicator.thermalChanged',
                 'com.apple.ManagedConfiguration.managedAppsChanged',
                 'com.apple.managedconfiguration.managedorginfochanged',
                 'com.apple.system.powermanagement.uservisiblepowerevent', 'com.apple.AirTunes.DACP.nextitem',
                 'com.apple.bookmarks.BookmarksFileChanged', 'com.apple.duetexpertd.prefschanged',
                 'com.apple.mobiletimerd.goodmorningtest', 'com.apple.bluetooth.connection',
                 'com.apple.VideosUI.UpNextRequestDidFinishNotification',
                 'com.apple.VideosUI.PlayHistoryUpdatedNotification',
                 'com.apple.proactive.PersonalizationPortrait.namedEntitiesInvalidated',
                 'com.apple.itunescloudd.artworkDownloadsDidCompleteNotification',
                 'com.apple.duetexpertd.ATXMMAppPredictor.IdleTimeEndAnchor',
                 'com.apple.Preferences.ResetPrivacyWarningsNotification',
                 'com.apple.siri.client.state.DynamiteClientState.siri_data_changed',
                 'com.apple.Preferences.ChangedRestrictionsEnabledStateNotification', 'com.apple.system.timezone',
                 'com.apple.commcenter.InternationalRoamingEDGE.changed', 'com.apple.duetexpertd.appclipprediction',
                 'com.apple.homed.user-cloud-share.wake.com.apple.applemediaservices.multiuser',
                 'com.apple.icloud.findmydeviced.findkit.magSafe.removed',
                 'com.apple.MobileAsset.Font7.ma.cached-metadata-updated',
                 'ApplePreferredContentSizeCategoryChangedNotification',
                 'com.apple.softwareupdate.autoinstall.startInstall',
                 'com.apple.corerecents.iCloudAccountChanged',
                 'com.apple.trial.NamespaceUpdate.NETWORK_SERVICE_PROXY_CONFIG_UPDATE',
                 'ACDAccountStoreDidChangeNotification', 'com.apple.triald.wake', 'VMStoreSetTokenNotification',
                 'com.apple.ap.adprivacyd.iTunesActiveAccountDidChangeNotification', 'com.apple.system.lowpowermode',
                 'com.apple.duet.expertcenter.appRefresh', 'com.apple.Sharing.prefsChanged',
                 'com.apple.system.thermalpressurelevel.cold', 'com.apple.siri.inference.coreduet-context',
                 'com.apple.mobile.keybagd.lock_status', 'com.apple.MobileAsset.EmbeddedSpeech.ma.new-asset-installed',
                 'com.apple.dataaccess.checkHolidayCalendarAccount',
                 'com.apple.softwareupdateservicesd.activity.autoDownload',
                 'com.apple.callhistorysync.idslaunchnotification',
                 'com.apple.ProtectedCloudStorage.test.mobileBackupStateChange',
                 'com.apple.voicetrigger.EarlyDetect', 'com.apple.AirTunes.DACP.volumedown',
                 'com.apple.timezonesync.idslaunchnotification', 'AppleTimePreferencesChangedNotification',
                 'com.apple.AirTunes.DACP.mutetoggle', 'com.apple.EscrowSecurityAlert.reset',
                 'com.apple.Carousel.wristStateChanged',
                 'com.apple.voicemail.changed', 'com.apple.duetexpertd.ATXAnchorModel.IdleTimeEndAnchor',
                 'dmf.policy.monitor.app',
                 'com.apple.coreaudio.speechDetectionVAD.created']


class NotificationProxyService(object):
    SERVICE_NAME = 'com.apple.mobile.notification_proxy'
    RSD_SERVICE_NAME = 'com.apple.mobile.notification_proxy.shim.remote'

    def __init__(self, lockdown=None, udid=None, network=None, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        self.lockdown = lockdown or LockdownClient(udid=udid, network=network)
        SERVICE_NAME = self.RSD_SERVICE_NAME if isinstance(self.lockdown,
                                                           RemoteLockdownClient) else self.SERVICE_NAME
        self.service = self.lockdown.start_service(SERVICE_NAME)

    def notify_post(self, name: str):
        self.service.send_plist({'Command': 'PostNotification',
                                 'Name': name})

    def notify_observe(self, name: str):
        self.logger.info('Observing %s', name)
        self.service.send_plist({'Command': 'ObserveNotification',
                                 'Name': name})

    def receive_notification(self):
        while True:
            yield self.service.recv_plist()


if __name__ == '__main__':
    service = NotificationProxyService()
    for notification in notifications:
        service.notify_observe(notification)
    for i in service.receive_notification():
        print(i)
