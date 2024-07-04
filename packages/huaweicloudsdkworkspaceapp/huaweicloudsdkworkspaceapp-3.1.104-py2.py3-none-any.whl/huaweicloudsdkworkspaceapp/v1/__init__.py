# coding: utf-8

from __future__ import absolute_import

from huaweicloudsdkworkspaceapp.v1.workspaceapp_client import WorkspaceAppClient
from huaweicloudsdkworkspaceapp.v1.workspaceapp_async_client import WorkspaceAppAsyncClient

from huaweicloudsdkworkspaceapp.v1.model.account_info import AccountInfo
from huaweicloudsdkworkspaceapp.v1.model.account_type_enum import AccountTypeEnum
from huaweicloudsdkworkspaceapp.v1.model.add_app_group_authorization_request import AddAppGroupAuthorizationRequest
from huaweicloudsdkworkspaceapp.v1.model.add_app_group_authorization_response import AddAppGroupAuthorizationResponse
from huaweicloudsdkworkspaceapp.v1.model.app import App
from huaweicloudsdkworkspaceapp.v1.model.app_connection_info import AppConnectionInfo
from huaweicloudsdkworkspaceapp.v1.model.app_group import AppGroup
from huaweicloudsdkworkspaceapp.v1.model.app_group_authorize_req import AppGroupAuthorizeReq
from huaweicloudsdkworkspaceapp.v1.model.app_server import AppServer
from huaweicloudsdkworkspaceapp.v1.model.app_server_status import AppServerStatus
from huaweicloudsdkworkspaceapp.v1.model.app_server_task_status import AppServerTaskStatus
from huaweicloudsdkworkspaceapp.v1.model.app_session import AppSession
from huaweicloudsdkworkspaceapp.v1.model.app_state_enum import AppStateEnum
from huaweicloudsdkworkspaceapp.v1.model.app_type_enum import AppTypeEnum
from huaweicloudsdkworkspaceapp.v1.model.assign_share_folder_req import AssignShareFolderReq
from huaweicloudsdkworkspaceapp.v1.model.assign_user_folder_req import AssignUserFolderReq
from huaweicloudsdkworkspaceapp.v1.model.assignment import Assignment
from huaweicloudsdkworkspaceapp.v1.model.attach_type import AttachType
from huaweicloudsdkworkspaceapp.v1.model.attachment import Attachment
from huaweicloudsdkworkspaceapp.v1.model.authorization import Authorization
from huaweicloudsdkworkspaceapp.v1.model.authorization_type_enum import AuthorizationTypeEnum
from huaweicloudsdkworkspaceapp.v1.model.auto_logout_options import AutoLogoutOptions
from huaweicloudsdkworkspaceapp.v1.model.availability_zone_info import AvailabilityZoneInfo
from huaweicloudsdkworkspaceapp.v1.model.bandwidth import Bandwidth
from huaweicloudsdkworkspaceapp.v1.model.base_app_group import BaseAppGroup
from huaweicloudsdkworkspaceapp.v1.model.base_server import BaseServer
from huaweicloudsdkworkspaceapp.v1.model.base_server_group import BaseServerGroup
from huaweicloudsdkworkspaceapp.v1.model.batch_delete_app_group_authorization_request import BatchDeleteAppGroupAuthorizationRequest
from huaweicloudsdkworkspaceapp.v1.model.batch_delete_app_group_authorization_response import BatchDeleteAppGroupAuthorizationResponse
from huaweicloudsdkworkspaceapp.v1.model.batch_delete_app_group_request import BatchDeleteAppGroupRequest
from huaweicloudsdkworkspaceapp.v1.model.batch_delete_app_group_response import BatchDeleteAppGroupResponse
from huaweicloudsdkworkspaceapp.v1.model.batch_delete_server_req import BatchDeleteServerReq
from huaweicloudsdkworkspaceapp.v1.model.batch_delete_server_request import BatchDeleteServerRequest
from huaweicloudsdkworkspaceapp.v1.model.batch_delete_server_response import BatchDeleteServerResponse
from huaweicloudsdkworkspaceapp.v1.model.batch_migrate_hosts_server_request import BatchMigrateHostsServerRequest
from huaweicloudsdkworkspaceapp.v1.model.batch_migrate_hosts_server_response import BatchMigrateHostsServerResponse
from huaweicloudsdkworkspaceapp.v1.model.batch_migrate_server_req import BatchMigrateServerReq
from huaweicloudsdkworkspaceapp.v1.model.batch_reboot_server_request import BatchRebootServerRequest
from huaweicloudsdkworkspaceapp.v1.model.batch_reboot_server_response import BatchRebootServerResponse
from huaweicloudsdkworkspaceapp.v1.model.batch_rejoin_domain_req import BatchRejoinDomainReq
from huaweicloudsdkworkspaceapp.v1.model.batch_rejoin_domain_request import BatchRejoinDomainRequest
from huaweicloudsdkworkspaceapp.v1.model.batch_rejoin_domain_response import BatchRejoinDomainResponse
from huaweicloudsdkworkspaceapp.v1.model.batch_start_server_req import BatchStartServerReq
from huaweicloudsdkworkspaceapp.v1.model.batch_start_server_request import BatchStartServerRequest
from huaweicloudsdkworkspaceapp.v1.model.batch_start_server_response import BatchStartServerResponse
from huaweicloudsdkworkspaceapp.v1.model.batch_stop_server_request import BatchStopServerRequest
from huaweicloudsdkworkspaceapp.v1.model.batch_stop_server_response import BatchStopServerResponse
from huaweicloudsdkworkspaceapp.v1.model.batch_update_tsvi_request import BatchUpdateTsviRequest
from huaweicloudsdkworkspaceapp.v1.model.batch_update_tsvi_response import BatchUpdateTsviResponse
from huaweicloudsdkworkspaceapp.v1.model.camera_bandwidth_control_options import CameraBandwidthControlOptions
from huaweicloudsdkworkspaceapp.v1.model.camera_bandwidth_percentage_options import CameraBandwidthPercentageOptions
from huaweicloudsdkworkspaceapp.v1.model.camera_redirection_options import CameraRedirectionOptions
from huaweicloudsdkworkspaceapp.v1.model.cbc_freeze_info import CbcFreezeInfo
from huaweicloudsdkworkspaceapp.v1.model.cbc_freeze_scene import CbcFreezeScene
from huaweicloudsdkworkspaceapp.v1.model.change_server_image_req import ChangeServerImageReq
from huaweicloudsdkworkspaceapp.v1.model.change_server_image_request import ChangeServerImageRequest
from huaweicloudsdkworkspaceapp.v1.model.change_server_image_response import ChangeServerImageResponse
from huaweicloudsdkworkspaceapp.v1.model.check_quota_request import CheckQuotaRequest
from huaweicloudsdkworkspaceapp.v1.model.check_quota_response import CheckQuotaResponse
from huaweicloudsdkworkspaceapp.v1.model.claim_mode import ClaimMode
from huaweicloudsdkworkspaceapp.v1.model.clipboard_bandwidth_control_options import ClipboardBandwidthControlOptions
from huaweicloudsdkworkspaceapp.v1.model.clipboard_bandwidth_percentage_options import ClipboardBandwidthPercentageOptions
from huaweicloudsdkworkspaceapp.v1.model.com_bandwidth_control_options import ComBandwidthControlOptions
from huaweicloudsdkworkspaceapp.v1.model.com_bandwidth_percentage_options import ComBandwidthPercentageOptions
from huaweicloudsdkworkspaceapp.v1.model.create_app_group_req import CreateAppGroupReq
from huaweicloudsdkworkspaceapp.v1.model.create_app_group_request import CreateAppGroupRequest
from huaweicloudsdkworkspaceapp.v1.model.create_app_group_response import CreateAppGroupResponse
from huaweicloudsdkworkspaceapp.v1.model.create_app_server_req import CreateAppServerReq
from huaweicloudsdkworkspaceapp.v1.model.create_app_servers_request import CreateAppServersRequest
from huaweicloudsdkworkspaceapp.v1.model.create_app_servers_response import CreateAppServersResponse
from huaweicloudsdkworkspaceapp.v1.model.create_or_update_storage_policy_statement_req import CreateOrUpdateStoragePolicyStatementReq
from huaweicloudsdkworkspaceapp.v1.model.create_or_update_storage_policy_statement_request import CreateOrUpdateStoragePolicyStatementRequest
from huaweicloudsdkworkspaceapp.v1.model.create_or_update_storage_policy_statement_response import CreateOrUpdateStoragePolicyStatementResponse
from huaweicloudsdkworkspaceapp.v1.model.create_persistent_storage_req import CreatePersistentStorageReq
from huaweicloudsdkworkspaceapp.v1.model.create_persistent_storage_request import CreatePersistentStorageRequest
from huaweicloudsdkworkspaceapp.v1.model.create_persistent_storage_response import CreatePersistentStorageResponse
from huaweicloudsdkworkspaceapp.v1.model.create_policy_group_req import CreatePolicyGroupReq
from huaweicloudsdkworkspaceapp.v1.model.create_policy_group_request import CreatePolicyGroupRequest
from huaweicloudsdkworkspaceapp.v1.model.create_policy_group_response import CreatePolicyGroupResponse
from huaweicloudsdkworkspaceapp.v1.model.create_policy_template_req import CreatePolicyTemplateReq
from huaweicloudsdkworkspaceapp.v1.model.create_policy_template_request import CreatePolicyTemplateRequest
from huaweicloudsdkworkspaceapp.v1.model.create_policy_template_response import CreatePolicyTemplateResponse
from huaweicloudsdkworkspaceapp.v1.model.create_server_extend_param import CreateServerExtendParam
from huaweicloudsdkworkspaceapp.v1.model.create_server_group_req import CreateServerGroupReq
from huaweicloudsdkworkspaceapp.v1.model.create_server_group_request import CreateServerGroupRequest
from huaweicloudsdkworkspaceapp.v1.model.create_server_group_response import CreateServerGroupResponse
from huaweicloudsdkworkspaceapp.v1.model.create_share_folder_req import CreateShareFolderReq
from huaweicloudsdkworkspaceapp.v1.model.create_share_folder_request import CreateShareFolderRequest
from huaweicloudsdkworkspaceapp.v1.model.create_share_folder_response import CreateShareFolderResponse
from huaweicloudsdkworkspaceapp.v1.model.custom_options import CustomOptions
from huaweicloudsdkworkspaceapp.v1.model.delete_app_group_req import DeleteAppGroupReq
from huaweicloudsdkworkspaceapp.v1.model.delete_persistent_storage_request import DeletePersistentStorageRequest
from huaweicloudsdkworkspaceapp.v1.model.delete_persistent_storage_response import DeletePersistentStorageResponse
from huaweicloudsdkworkspaceapp.v1.model.delete_policy_group_request import DeletePolicyGroupRequest
from huaweicloudsdkworkspaceapp.v1.model.delete_policy_group_response import DeletePolicyGroupResponse
from huaweicloudsdkworkspaceapp.v1.model.delete_policy_template_request import DeletePolicyTemplateRequest
from huaweicloudsdkworkspaceapp.v1.model.delete_policy_template_response import DeletePolicyTemplateResponse
from huaweicloudsdkworkspaceapp.v1.model.delete_server_groups_request import DeleteServerGroupsRequest
from huaweicloudsdkworkspaceapp.v1.model.delete_server_groups_response import DeleteServerGroupsResponse
from huaweicloudsdkworkspaceapp.v1.model.delete_storage_claim_req import DeleteStorageClaimReq
from huaweicloudsdkworkspaceapp.v1.model.delete_storage_claim_request import DeleteStorageClaimRequest
from huaweicloudsdkworkspaceapp.v1.model.delete_storage_claim_response import DeleteStorageClaimResponse
from huaweicloudsdkworkspaceapp.v1.model.delete_user_storage_attachment_req import DeleteUserStorageAttachmentReq
from huaweicloudsdkworkspaceapp.v1.model.delete_user_storage_attachment_request import DeleteUserStorageAttachmentRequest
from huaweicloudsdkworkspaceapp.v1.model.delete_user_storage_attachment_response import DeleteUserStorageAttachmentResponse
from huaweicloudsdkworkspaceapp.v1.model.display_bandwidth_control_options import DisplayBandwidthControlOptions
from huaweicloudsdkworkspaceapp.v1.model.display_bandwidth_percentage_options import DisplayBandwidthPercentageOptions
from huaweicloudsdkworkspaceapp.v1.model.display_options import DisplayOptions
from huaweicloudsdkworkspaceapp.v1.model.display_options_deep_compression_options import DisplayOptionsDeepCompressionOptions
from huaweicloudsdkworkspaceapp.v1.model.display_options_video_bit_rate_options import DisplayOptionsVideoBitRateOptions
from huaweicloudsdkworkspaceapp.v1.model.display_options_video_quality_options import DisplayOptionsVideoQualityOptions
from huaweicloudsdkworkspaceapp.v1.model.ecs_net_work import EcsNetWork
from huaweicloudsdkworkspaceapp.v1.model.extra_session_type_enum import ExtraSessionTypeEnum
from huaweicloudsdkworkspaceapp.v1.model.file_redirection_bandwidth_control_options import FileRedirectionBandwidthControlOptions
from huaweicloudsdkworkspaceapp.v1.model.file_redirection_bandwidth_percentage_options import FileRedirectionBandwidthPercentageOptions
from huaweicloudsdkworkspaceapp.v1.model.file_redirection_options import FileRedirectionOptions
from huaweicloudsdkworkspaceapp.v1.model.file_redirection_options_compression_switch_options import FileRedirectionOptionsCompressionSwitchOptions
from huaweicloudsdkworkspaceapp.v1.model.file_redirection_options_fluid_control_options import FileRedirectionOptionsFluidControlOptions
from huaweicloudsdkworkspaceapp.v1.model.file_redirection_options_linux_file_size_supported_options import FileRedirectionOptionsLinuxFileSizeSupportedOptions
from huaweicloudsdkworkspaceapp.v1.model.flavor import Flavor
from huaweicloudsdkworkspaceapp.v1.model.flavor_link import FlavorLink
from huaweicloudsdkworkspaceapp.v1.model.i18n import I18n
from huaweicloudsdkworkspaceapp.v1.model.image_type_enum import ImageTypeEnum
from huaweicloudsdkworkspaceapp.v1.model.ip_virtual import IpVirtual
from huaweicloudsdkworkspaceapp.v1.model.job_detail import JobDetail
from huaweicloudsdkworkspaceapp.v1.model.job_detail_info import JobDetailInfo
from huaweicloudsdkworkspaceapp.v1.model.job_detail_status import JobDetailStatus
from huaweicloudsdkworkspaceapp.v1.model.job_id_info import JobIdInfo
from huaweicloudsdkworkspaceapp.v1.model.job_info import JobInfo
from huaweicloudsdkworkspaceapp.v1.model.job_resource_info import JobResourceInfo
from huaweicloudsdkworkspaceapp.v1.model.job_status import JobStatus
from huaweicloudsdkworkspaceapp.v1.model.job_type import JobType
from huaweicloudsdkworkspaceapp.v1.model.list_app_connection_req import ListAppConnectionReq
from huaweicloudsdkworkspaceapp.v1.model.list_app_connection_request import ListAppConnectionRequest
from huaweicloudsdkworkspaceapp.v1.model.list_app_connection_response import ListAppConnectionResponse
from huaweicloudsdkworkspaceapp.v1.model.list_app_group_authorization_request import ListAppGroupAuthorizationRequest
from huaweicloudsdkworkspaceapp.v1.model.list_app_group_authorization_response import ListAppGroupAuthorizationResponse
from huaweicloudsdkworkspaceapp.v1.model.list_app_group_request import ListAppGroupRequest
from huaweicloudsdkworkspaceapp.v1.model.list_app_group_response import ListAppGroupResponse
from huaweicloudsdkworkspaceapp.v1.model.list_availability_zone_request import ListAvailabilityZoneRequest
from huaweicloudsdkworkspaceapp.v1.model.list_availability_zone_response import ListAvailabilityZoneResponse
from huaweicloudsdkworkspaceapp.v1.model.list_persistent_storage_request import ListPersistentStorageRequest
from huaweicloudsdkworkspaceapp.v1.model.list_persistent_storage_response import ListPersistentStorageResponse
from huaweicloudsdkworkspaceapp.v1.model.list_policy_group_request import ListPolicyGroupRequest
from huaweicloudsdkworkspaceapp.v1.model.list_policy_group_response import ListPolicyGroupResponse
from huaweicloudsdkworkspaceapp.v1.model.list_policy_template_request import ListPolicyTemplateRequest
from huaweicloudsdkworkspaceapp.v1.model.list_policy_template_response import ListPolicyTemplateResponse
from huaweicloudsdkworkspaceapp.v1.model.list_product_request import ListProductRequest
from huaweicloudsdkworkspaceapp.v1.model.list_product_response import ListProductResponse
from huaweicloudsdkworkspaceapp.v1.model.list_published_app_request import ListPublishedAppRequest
from huaweicloudsdkworkspaceapp.v1.model.list_published_app_response import ListPublishedAppResponse
from huaweicloudsdkworkspaceapp.v1.model.list_server_groups_request import ListServerGroupsRequest
from huaweicloudsdkworkspaceapp.v1.model.list_server_groups_response import ListServerGroupsResponse
from huaweicloudsdkworkspaceapp.v1.model.list_servers_request import ListServersRequest
from huaweicloudsdkworkspaceapp.v1.model.list_servers_response import ListServersResponse
from huaweicloudsdkworkspaceapp.v1.model.list_session_by_user_name_request import ListSessionByUserNameRequest
from huaweicloudsdkworkspaceapp.v1.model.list_session_by_user_name_response import ListSessionByUserNameResponse
from huaweicloudsdkworkspaceapp.v1.model.list_session_type_request import ListSessionTypeRequest
from huaweicloudsdkworkspaceapp.v1.model.list_session_type_response import ListSessionTypeResponse
from huaweicloudsdkworkspaceapp.v1.model.list_share_folder_request import ListShareFolderRequest
from huaweicloudsdkworkspaceapp.v1.model.list_share_folder_response import ListShareFolderResponse
from huaweicloudsdkworkspaceapp.v1.model.list_storage_assignment_request import ListStorageAssignmentRequest
from huaweicloudsdkworkspaceapp.v1.model.list_storage_assignment_response import ListStorageAssignmentResponse
from huaweicloudsdkworkspaceapp.v1.model.list_storage_policy_statement_request import ListStoragePolicyStatementRequest
from huaweicloudsdkworkspaceapp.v1.model.list_storage_policy_statement_response import ListStoragePolicyStatementResponse
from huaweicloudsdkworkspaceapp.v1.model.list_targets_of_policy_group_request import ListTargetsOfPolicyGroupRequest
from huaweicloudsdkworkspaceapp.v1.model.list_targets_of_policy_group_response import ListTargetsOfPolicyGroupResponse
from huaweicloudsdkworkspaceapp.v1.model.list_user_connection_req import ListUserConnectionReq
from huaweicloudsdkworkspaceapp.v1.model.list_user_connection_request import ListUserConnectionRequest
from huaweicloudsdkworkspaceapp.v1.model.list_user_connection_response import ListUserConnectionResponse
from huaweicloudsdkworkspaceapp.v1.model.list_volume_type_request import ListVolumeTypeRequest
from huaweicloudsdkworkspaceapp.v1.model.list_volume_type_response import ListVolumeTypeResponse
from huaweicloudsdkworkspaceapp.v1.model.logoff_user_session_req import LogoffUserSessionReq
from huaweicloudsdkworkspaceapp.v1.model.logoff_user_session_request import LogoffUserSessionRequest
from huaweicloudsdkworkspaceapp.v1.model.logoff_user_session_response import LogoffUserSessionResponse
from huaweicloudsdkworkspaceapp.v1.model.multimedia_bandwidth_control_options import MultimediaBandwidthControlOptions
from huaweicloudsdkworkspaceapp.v1.model.multimedia_bandwidth_percentage_options import MultimediaBandwidthPercentageOptions
from huaweicloudsdkworkspaceapp.v1.model.nic import Nic
from huaweicloudsdkworkspaceapp.v1.model.os_type_enum import OsTypeEnum
from huaweicloudsdkworkspaceapp.v1.model.page_resp import PageResp
from huaweicloudsdkworkspaceapp.v1.model.pcsc_bandwidth_control_options import PcscBandwidthControlOptions
from huaweicloudsdkworkspaceapp.v1.model.pcsc_bandwidth_percentage_options import PcscBandwidthPercentageOptions
from huaweicloudsdkworkspaceapp.v1.model.persistent_storage import PersistentStorage
from huaweicloudsdkworkspaceapp.v1.model.persistent_storage_assignment import PersistentStorageAssignment
from huaweicloudsdkworkspaceapp.v1.model.persistent_storage_claim import PersistentStorageClaim
from huaweicloudsdkworkspaceapp.v1.model.platform_type_enum import PlatformTypeEnum
from huaweicloudsdkworkspaceapp.v1.model.policies import Policies
from huaweicloudsdkworkspaceapp.v1.model.policies_audio import PoliciesAudio
from huaweicloudsdkworkspaceapp.v1.model.policies_client import PoliciesClient
from huaweicloudsdkworkspaceapp.v1.model.policies_custom import PoliciesCustom
from huaweicloudsdkworkspaceapp.v1.model.policies_display import PoliciesDisplay
from huaweicloudsdkworkspaceapp.v1.model.policies_display_rendering_acceleration_options import PoliciesDisplayRenderingAccelerationOptions
from huaweicloudsdkworkspaceapp.v1.model.policies_file_and_clipboard import PoliciesFileAndClipboard
from huaweicloudsdkworkspaceapp.v1.model.policies_file_and_clipboard_clipboard_redirection_options import PoliciesFileAndClipboardClipboardRedirectionOptions
from huaweicloudsdkworkspaceapp.v1.model.policies_file_and_clipboard_file_redirection import PoliciesFileAndClipboardFileRedirection
from huaweicloudsdkworkspaceapp.v1.model.policies_file_and_clipboard_file_redirection_redirection_send_file_options import PoliciesFileAndClipboardFileRedirectionRedirectionSendFileOptions
from huaweicloudsdkworkspaceapp.v1.model.policies_keyboard_mouse import PoliciesKeyboardMouse
from huaweicloudsdkworkspaceapp.v1.model.policies_peripherals import PoliciesPeripherals
from huaweicloudsdkworkspaceapp.v1.model.policies_peripherals_device_redirection import PoliciesPeripheralsDeviceRedirection
from huaweicloudsdkworkspaceapp.v1.model.policies_peripherals_device_redirection_camera_redirection import PoliciesPeripheralsDeviceRedirectionCameraRedirection
from huaweicloudsdkworkspaceapp.v1.model.policies_peripherals_device_redirection_printer_redirection import PoliciesPeripheralsDeviceRedirectionPrinterRedirection
from huaweicloudsdkworkspaceapp.v1.model.policies_peripherals_device_redirection_session_printer import PoliciesPeripheralsDeviceRedirectionSessionPrinter
from huaweicloudsdkworkspaceapp.v1.model.policies_peripherals_serial_port_redirection import PoliciesPeripheralsSerialPortRedirection
from huaweicloudsdkworkspaceapp.v1.model.policies_peripherals_usb_device_common import PoliciesPeripheralsUsbDeviceCommon
from huaweicloudsdkworkspaceapp.v1.model.policies_peripherals_usb_device_common_common_options import PoliciesPeripheralsUsbDeviceCommonCommonOptions
from huaweicloudsdkworkspaceapp.v1.model.policies_peripherals_usb_port_redirection import PoliciesPeripheralsUsbPortRedirection
from huaweicloudsdkworkspaceapp.v1.model.policy_group import PolicyGroup
from huaweicloudsdkworkspaceapp.v1.model.policy_group_for_create import PolicyGroupForCreate
from huaweicloudsdkworkspaceapp.v1.model.policy_group_for_update import PolicyGroupForUpdate
from huaweicloudsdkworkspaceapp.v1.model.policy_statement import PolicyStatement
from huaweicloudsdkworkspaceapp.v1.model.policy_template import PolicyTemplate
from huaweicloudsdkworkspaceapp.v1.model.printer_bandwidth_control_options import PrinterBandwidthControlOptions
from huaweicloudsdkworkspaceapp.v1.model.printer_bandwidth_percentage_options import PrinterBandwidthPercentageOptions
from huaweicloudsdkworkspaceapp.v1.model.printer_redirection_options import PrinterRedirectionOptions
from huaweicloudsdkworkspaceapp.v1.model.product_info import ProductInfo
from huaweicloudsdkworkspaceapp.v1.model.publish_app import PublishApp
from huaweicloudsdkworkspaceapp.v1.model.publish_app_req import PublishAppReq
from huaweicloudsdkworkspaceapp.v1.model.publish_app_request import PublishAppRequest
from huaweicloudsdkworkspaceapp.v1.model.publish_app_response import PublishAppResponse
from huaweicloudsdkworkspaceapp.v1.model.publishable_app import PublishableApp
from huaweicloudsdkworkspaceapp.v1.model.quota_remainder_data import QuotaRemainderData
from huaweicloudsdkworkspaceapp.v1.model.quota_resource_type_enum import QuotaResourceTypeEnum
from huaweicloudsdkworkspaceapp.v1.model.reinstall_server_req import ReinstallServerReq
from huaweicloudsdkworkspaceapp.v1.model.reinstall_server_request import ReinstallServerRequest
from huaweicloudsdkworkspaceapp.v1.model.reinstall_server_response import ReinstallServerResponse
from huaweicloudsdkworkspaceapp.v1.model.relative_resource import RelativeResource
from huaweicloudsdkworkspaceapp.v1.model.route_policy import RoutePolicy
from huaweicloudsdkworkspaceapp.v1.model.sbc import Sbc
from huaweicloudsdkworkspaceapp.v1.model.sbc_automatic_disconnection_options import SbcAutomaticDisconnectionOptions
from huaweicloudsdkworkspaceapp.v1.model.scaling_policy import ScalingPolicy
from huaweicloudsdkworkspaceapp.v1.model.scaling_policy_by_session import ScalingPolicyBySession
from huaweicloudsdkworkspaceapp.v1.model.secure_channel_bandwidth_control_options import SecureChannelBandwidthControlOptions
from huaweicloudsdkworkspaceapp.v1.model.secure_channel_bandwidth_percentage_options import SecureChannelBandwidthPercentageOptions
from huaweicloudsdkworkspaceapp.v1.model.serial_port_redirection_options import SerialPortRedirectionOptions
from huaweicloudsdkworkspaceapp.v1.model.server_address import ServerAddress
from huaweicloudsdkworkspaceapp.v1.model.server_group import ServerGroup
from huaweicloudsdkworkspaceapp.v1.model.server_halt_req import ServerHaltReq
from huaweicloudsdkworkspaceapp.v1.model.server_halt_type import ServerHaltType
from huaweicloudsdkworkspaceapp.v1.model.server_id_set import ServerIdSet
from huaweicloudsdkworkspaceapp.v1.model.server_status import ServerStatus
from huaweicloudsdkworkspaceapp.v1.model.session import Session
from huaweicloudsdkworkspaceapp.v1.model.session_printer_options import SessionPrinterOptions
from huaweicloudsdkworkspaceapp.v1.model.session_type_entity import SessionTypeEntity
from huaweicloudsdkworkspaceapp.v1.model.share_persistent_storage_claim import SharePersistentStorageClaim
from huaweicloudsdkworkspaceapp.v1.model.show_job_detail_request import ShowJobDetailRequest
from huaweicloudsdkworkspaceapp.v1.model.show_job_detail_response import ShowJobDetailResponse
from huaweicloudsdkworkspaceapp.v1.model.show_job_request import ShowJobRequest
from huaweicloudsdkworkspaceapp.v1.model.show_job_response import ShowJobResponse
from huaweicloudsdkworkspaceapp.v1.model.show_original_policy_info_request import ShowOriginalPolicyInfoRequest
from huaweicloudsdkworkspaceapp.v1.model.show_original_policy_info_response import ShowOriginalPolicyInfoResponse
from huaweicloudsdkworkspaceapp.v1.model.show_publishable_app_request import ShowPublishableAppRequest
from huaweicloudsdkworkspaceapp.v1.model.show_publishable_app_response import ShowPublishableAppResponse
from huaweicloudsdkworkspaceapp.v1.model.sold_out_info import SoldOutInfo
from huaweicloudsdkworkspaceapp.v1.model.storage import Storage
from huaweicloudsdkworkspaceapp.v1.model.storage_folder_mount_type import StorageFolderMountType
from huaweicloudsdkworkspaceapp.v1.model.storage_metadata import StorageMetadata
from huaweicloudsdkworkspaceapp.v1.model.string_set import StringSet
from huaweicloudsdkworkspaceapp.v1.model.sub_job_info import SubJobInfo
from huaweicloudsdkworkspaceapp.v1.model.target import Target
from huaweicloudsdkworkspaceapp.v1.model.total_bandwidth_control_options import TotalBandwidthControlOptions
from huaweicloudsdkworkspaceapp.v1.model.twain_bandwidth_control_options import TwainBandwidthControlOptions
from huaweicloudsdkworkspaceapp.v1.model.twain_bandwidth_percentage_options import TwainBandwidthPercentageOptions
from huaweicloudsdkworkspaceapp.v1.model.unpublish_app_req import UnpublishAppReq
from huaweicloudsdkworkspaceapp.v1.model.unpublish_app_request import UnpublishAppRequest
from huaweicloudsdkworkspaceapp.v1.model.unpublish_app_response import UnpublishAppResponse
from huaweicloudsdkworkspaceapp.v1.model.update_app_group_req import UpdateAppGroupReq
from huaweicloudsdkworkspaceapp.v1.model.update_app_group_request import UpdateAppGroupRequest
from huaweicloudsdkworkspaceapp.v1.model.update_app_group_response import UpdateAppGroupResponse
from huaweicloudsdkworkspaceapp.v1.model.update_app_req import UpdateAppReq
from huaweicloudsdkworkspaceapp.v1.model.update_app_request import UpdateAppRequest
from huaweicloudsdkworkspaceapp.v1.model.update_app_response import UpdateAppResponse
from huaweicloudsdkworkspaceapp.v1.model.update_policy_group_req import UpdatePolicyGroupReq
from huaweicloudsdkworkspaceapp.v1.model.update_policy_group_request import UpdatePolicyGroupRequest
from huaweicloudsdkworkspaceapp.v1.model.update_policy_group_response import UpdatePolicyGroupResponse
from huaweicloudsdkworkspaceapp.v1.model.update_policy_template_req import UpdatePolicyTemplateReq
from huaweicloudsdkworkspaceapp.v1.model.update_policy_template_request import UpdatePolicyTemplateRequest
from huaweicloudsdkworkspaceapp.v1.model.update_policy_template_response import UpdatePolicyTemplateResponse
from huaweicloudsdkworkspaceapp.v1.model.update_server_group_req import UpdateServerGroupReq
from huaweicloudsdkworkspaceapp.v1.model.update_server_group_request import UpdateServerGroupRequest
from huaweicloudsdkworkspaceapp.v1.model.update_server_group_response import UpdateServerGroupResponse
from huaweicloudsdkworkspaceapp.v1.model.update_server_req import UpdateServerReq
from huaweicloudsdkworkspaceapp.v1.model.update_server_request import UpdateServerRequest
from huaweicloudsdkworkspaceapp.v1.model.update_server_response import UpdateServerResponse
from huaweicloudsdkworkspaceapp.v1.model.update_share_folder_assignment_request import UpdateShareFolderAssignmentRequest
from huaweicloudsdkworkspaceapp.v1.model.update_share_folder_assignment_response import UpdateShareFolderAssignmentResponse
from huaweicloudsdkworkspaceapp.v1.model.update_tsvi import UpdateTsvi
from huaweicloudsdkworkspaceapp.v1.model.update_tsvi_req import UpdateTsviReq
from huaweicloudsdkworkspaceapp.v1.model.update_user_folder_assignment_request import UpdateUserFolderAssignmentRequest
from huaweicloudsdkworkspaceapp.v1.model.update_user_folder_assignment_response import UpdateUserFolderAssignmentResponse
from huaweicloudsdkworkspaceapp.v1.model.upload_app_icon_request import UploadAppIconRequest
from huaweicloudsdkworkspaceapp.v1.model.upload_app_icon_request_body import UploadAppIconRequestBody
from huaweicloudsdkworkspaceapp.v1.model.upload_app_icon_response import UploadAppIconResponse
from huaweicloudsdkworkspaceapp.v1.model.usb_bandwidth_control_options import UsbBandwidthControlOptions
from huaweicloudsdkworkspaceapp.v1.model.usb_bandwidth_percentage_options import UsbBandwidthPercentageOptions
from huaweicloudsdkworkspaceapp.v1.model.usb_port_redirection_options import UsbPortRedirectionOptions
from huaweicloudsdkworkspaceapp.v1.model.user_assignment import UserAssignment
from huaweicloudsdkworkspaceapp.v1.model.user_connection_info import UserConnectionInfo
from huaweicloudsdkworkspaceapp.v1.model.virtual_channel import VirtualChannel
from huaweicloudsdkworkspaceapp.v1.model.virtual_channel_bandwidth_control_options import VirtualChannelBandwidthControlOptions
from huaweicloudsdkworkspaceapp.v1.model.virtual_channel_bandwidth_percentage_options import VirtualChannelBandwidthPercentageOptions
from huaweicloudsdkworkspaceapp.v1.model.virtual_channel_options import VirtualChannelOptions
from huaweicloudsdkworkspaceapp.v1.model.volume import Volume
from huaweicloudsdkworkspaceapp.v1.model.volume_type import VolumeType
from huaweicloudsdkworkspaceapp.v1.model.volume_type_extra_specs import VolumeTypeExtraSpecs
from huaweicloudsdkworkspaceapp.v1.model.volume_type_info import VolumeTypeInfo
from huaweicloudsdkworkspaceapp.v1.model.wdh_param import WdhParam

