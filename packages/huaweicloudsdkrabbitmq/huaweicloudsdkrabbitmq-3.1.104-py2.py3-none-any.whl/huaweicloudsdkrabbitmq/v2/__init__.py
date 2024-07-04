# coding: utf-8

from __future__ import absolute_import

from huaweicloudsdkrabbitmq.v2.rabbitmq_client import RabbitMQClient
from huaweicloudsdkrabbitmq.v2.rabbitmq_async_client import RabbitMQAsyncClient

from huaweicloudsdkrabbitmq.v2.model.amqp_user import AMQPUser
from huaweicloudsdkrabbitmq.v2.model.amqp_user_perm import AMQPUserPerm
from huaweicloudsdkrabbitmq.v2.model.batch_create_or_delete_rabbit_mq_tag_request import BatchCreateOrDeleteRabbitMqTagRequest
from huaweicloudsdkrabbitmq.v2.model.batch_create_or_delete_rabbit_mq_tag_response import BatchCreateOrDeleteRabbitMqTagResponse
from huaweicloudsdkrabbitmq.v2.model.batch_create_or_delete_tag_req import BatchCreateOrDeleteTagReq
from huaweicloudsdkrabbitmq.v2.model.batch_delete_body import BatchDeleteBody
from huaweicloudsdkrabbitmq.v2.model.batch_delete_exchanges_request import BatchDeleteExchangesRequest
from huaweicloudsdkrabbitmq.v2.model.batch_delete_exchanges_response import BatchDeleteExchangesResponse
from huaweicloudsdkrabbitmq.v2.model.batch_delete_queues_request import BatchDeleteQueuesRequest
from huaweicloudsdkrabbitmq.v2.model.batch_delete_queues_response import BatchDeleteQueuesResponse
from huaweicloudsdkrabbitmq.v2.model.batch_delete_vhosts_request import BatchDeleteVhostsRequest
from huaweicloudsdkrabbitmq.v2.model.batch_delete_vhosts_response import BatchDeleteVhostsResponse
from huaweicloudsdkrabbitmq.v2.model.batch_restart_or_delete_instance_req import BatchRestartOrDeleteInstanceReq
from huaweicloudsdkrabbitmq.v2.model.batch_restart_or_delete_instance_resp_results import BatchRestartOrDeleteInstanceRespResults
from huaweicloudsdkrabbitmq.v2.model.batch_restart_or_delete_instances_request import BatchRestartOrDeleteInstancesRequest
from huaweicloudsdkrabbitmq.v2.model.batch_restart_or_delete_instances_response import BatchRestartOrDeleteInstancesResponse
from huaweicloudsdkrabbitmq.v2.model.bindings_details import BindingsDetails
from huaweicloudsdkrabbitmq.v2.model.bss_param import BssParam
from huaweicloudsdkrabbitmq.v2.model.channel_details import ChannelDetails
from huaweicloudsdkrabbitmq.v2.model.consumer_details import ConsumerDetails
from huaweicloudsdkrabbitmq.v2.model.create_binding_body import CreateBindingBody
from huaweicloudsdkrabbitmq.v2.model.create_binding_request import CreateBindingRequest
from huaweicloudsdkrabbitmq.v2.model.create_binding_response import CreateBindingResponse
from huaweicloudsdkrabbitmq.v2.model.create_exchange_body import CreateExchangeBody
from huaweicloudsdkrabbitmq.v2.model.create_exchange_request import CreateExchangeRequest
from huaweicloudsdkrabbitmq.v2.model.create_exchange_response import CreateExchangeResponse
from huaweicloudsdkrabbitmq.v2.model.create_instance_req import CreateInstanceReq
from huaweicloudsdkrabbitmq.v2.model.create_post_paid_instance_by_engine_request import CreatePostPaidInstanceByEngineRequest
from huaweicloudsdkrabbitmq.v2.model.create_post_paid_instance_by_engine_response import CreatePostPaidInstanceByEngineResponse
from huaweicloudsdkrabbitmq.v2.model.create_post_paid_instance_request import CreatePostPaidInstanceRequest
from huaweicloudsdkrabbitmq.v2.model.create_post_paid_instance_response import CreatePostPaidInstanceResponse
from huaweicloudsdkrabbitmq.v2.model.create_queue_body import CreateQueueBody
from huaweicloudsdkrabbitmq.v2.model.create_queue_request import CreateQueueRequest
from huaweicloudsdkrabbitmq.v2.model.create_queue_response import CreateQueueResponse
from huaweicloudsdkrabbitmq.v2.model.create_user_request import CreateUserRequest
from huaweicloudsdkrabbitmq.v2.model.create_user_response import CreateUserResponse
from huaweicloudsdkrabbitmq.v2.model.create_vhost_body import CreateVhostBody
from huaweicloudsdkrabbitmq.v2.model.create_vhost_request import CreateVhostRequest
from huaweicloudsdkrabbitmq.v2.model.create_vhost_response import CreateVhostResponse
from huaweicloudsdkrabbitmq.v2.model.delete_background_task_request import DeleteBackgroundTaskRequest
from huaweicloudsdkrabbitmq.v2.model.delete_background_task_response import DeleteBackgroundTaskResponse
from huaweicloudsdkrabbitmq.v2.model.delete_binding_request import DeleteBindingRequest
from huaweicloudsdkrabbitmq.v2.model.delete_binding_response import DeleteBindingResponse
from huaweicloudsdkrabbitmq.v2.model.delete_instance_request import DeleteInstanceRequest
from huaweicloudsdkrabbitmq.v2.model.delete_instance_response import DeleteInstanceResponse
from huaweicloudsdkrabbitmq.v2.model.delete_queue_info_request import DeleteQueueInfoRequest
from huaweicloudsdkrabbitmq.v2.model.delete_queue_info_response import DeleteQueueInfoResponse
from huaweicloudsdkrabbitmq.v2.model.delete_user_request import DeleteUserRequest
from huaweicloudsdkrabbitmq.v2.model.delete_user_response import DeleteUserResponse
from huaweicloudsdkrabbitmq.v2.model.exchange_details import ExchangeDetails
from huaweicloudsdkrabbitmq.v2.model.list_available_zones_request import ListAvailableZonesRequest
from huaweicloudsdkrabbitmq.v2.model.list_available_zones_resp_available_zones import ListAvailableZonesRespAvailableZones
from huaweicloudsdkrabbitmq.v2.model.list_available_zones_response import ListAvailableZonesResponse
from huaweicloudsdkrabbitmq.v2.model.list_background_tasks_request import ListBackgroundTasksRequest
from huaweicloudsdkrabbitmq.v2.model.list_background_tasks_resp_tasks import ListBackgroundTasksRespTasks
from huaweicloudsdkrabbitmq.v2.model.list_background_tasks_response import ListBackgroundTasksResponse
from huaweicloudsdkrabbitmq.v2.model.list_bindings_request import ListBindingsRequest
from huaweicloudsdkrabbitmq.v2.model.list_bindings_response import ListBindingsResponse
from huaweicloudsdkrabbitmq.v2.model.list_engine_ios_entity import ListEngineIosEntity
from huaweicloudsdkrabbitmq.v2.model.list_engine_products_entity import ListEngineProductsEntity
from huaweicloudsdkrabbitmq.v2.model.list_engine_products_request import ListEngineProductsRequest
from huaweicloudsdkrabbitmq.v2.model.list_engine_products_response import ListEngineProductsResponse
from huaweicloudsdkrabbitmq.v2.model.list_engine_properties_entity import ListEnginePropertiesEntity
from huaweicloudsdkrabbitmq.v2.model.list_exchanges_request import ListExchangesRequest
from huaweicloudsdkrabbitmq.v2.model.list_exchanges_response import ListExchangesResponse
from huaweicloudsdkrabbitmq.v2.model.list_instances_details_request import ListInstancesDetailsRequest
from huaweicloudsdkrabbitmq.v2.model.list_instances_details_response import ListInstancesDetailsResponse
from huaweicloudsdkrabbitmq.v2.model.list_plugins_request import ListPluginsRequest
from huaweicloudsdkrabbitmq.v2.model.list_plugins_response import ListPluginsResponse
from huaweicloudsdkrabbitmq.v2.model.list_products_request import ListProductsRequest
from huaweicloudsdkrabbitmq.v2.model.list_products_resp_detail import ListProductsRespDetail
from huaweicloudsdkrabbitmq.v2.model.list_products_resp_hourly import ListProductsRespHourly
from huaweicloudsdkrabbitmq.v2.model.list_products_resp_io import ListProductsRespIo
from huaweicloudsdkrabbitmq.v2.model.list_products_resp_values import ListProductsRespValues
from huaweicloudsdkrabbitmq.v2.model.list_products_response import ListProductsResponse
from huaweicloudsdkrabbitmq.v2.model.list_queues_request import ListQueuesRequest
from huaweicloudsdkrabbitmq.v2.model.list_queues_response import ListQueuesResponse
from huaweicloudsdkrabbitmq.v2.model.list_user_request import ListUserRequest
from huaweicloudsdkrabbitmq.v2.model.list_user_response import ListUserResponse
from huaweicloudsdkrabbitmq.v2.model.list_vhosts_request import ListVhostsRequest
from huaweicloudsdkrabbitmq.v2.model.list_vhosts_response import ListVhostsResponse
from huaweicloudsdkrabbitmq.v2.model.maintain_windows_entity import MaintainWindowsEntity
from huaweicloudsdkrabbitmq.v2.model.plugin_entity import PluginEntity
from huaweicloudsdkrabbitmq.v2.model.queue_arguments import QueueArguments
from huaweicloudsdkrabbitmq.v2.model.queue_details import QueueDetails
from huaweicloudsdkrabbitmq.v2.model.rabbit_mq_extend_product_info_entity import RabbitMQExtendProductInfoEntity
from huaweicloudsdkrabbitmq.v2.model.rabbit_mq_extend_product_ios_entity import RabbitMQExtendProductIosEntity
from huaweicloudsdkrabbitmq.v2.model.rabbit_mq_extend_product_properties_entity import RabbitMQExtendProductPropertiesEntity
from huaweicloudsdkrabbitmq.v2.model.rabbit_mq_product_support_features_entity import RabbitMQProductSupportFeaturesEntity
from huaweicloudsdkrabbitmq.v2.model.reset_password_req import ResetPasswordReq
from huaweicloudsdkrabbitmq.v2.model.reset_password_request import ResetPasswordRequest
from huaweicloudsdkrabbitmq.v2.model.reset_password_response import ResetPasswordResponse
from huaweicloudsdkrabbitmq.v2.model.resize_engine_instance_req import ResizeEngineInstanceReq
from huaweicloudsdkrabbitmq.v2.model.resize_engine_instance_request import ResizeEngineInstanceRequest
from huaweicloudsdkrabbitmq.v2.model.resize_engine_instance_response import ResizeEngineInstanceResponse
from huaweicloudsdkrabbitmq.v2.model.resize_instance_req import ResizeInstanceReq
from huaweicloudsdkrabbitmq.v2.model.resize_instance_request import ResizeInstanceRequest
from huaweicloudsdkrabbitmq.v2.model.resize_instance_response import ResizeInstanceResponse
from huaweicloudsdkrabbitmq.v2.model.show_background_task_request import ShowBackgroundTaskRequest
from huaweicloudsdkrabbitmq.v2.model.show_background_task_response import ShowBackgroundTaskResponse
from huaweicloudsdkrabbitmq.v2.model.show_ces_hierarchy_request import ShowCesHierarchyRequest
from huaweicloudsdkrabbitmq.v2.model.show_ces_hierarchy_response import ShowCesHierarchyResponse
from huaweicloudsdkrabbitmq.v2.model.show_ceshierarchy_resp_children import ShowCeshierarchyRespChildren
from huaweicloudsdkrabbitmq.v2.model.show_ceshierarchy_resp_dimensions import ShowCeshierarchyRespDimensions
from huaweicloudsdkrabbitmq.v2.model.show_ceshierarchy_resp_exchanges import ShowCeshierarchyRespExchanges
from huaweicloudsdkrabbitmq.v2.model.show_ceshierarchy_resp_groups import ShowCeshierarchyRespGroups
from huaweicloudsdkrabbitmq.v2.model.show_ceshierarchy_resp_instance_ids import ShowCeshierarchyRespInstanceIds
from huaweicloudsdkrabbitmq.v2.model.show_ceshierarchy_resp_nodes import ShowCeshierarchyRespNodes
from huaweicloudsdkrabbitmq.v2.model.show_ceshierarchy_resp_queues import ShowCeshierarchyRespQueues
from huaweicloudsdkrabbitmq.v2.model.show_ceshierarchy_resp_vhosts import ShowCeshierarchyRespVhosts
from huaweicloudsdkrabbitmq.v2.model.show_engine_instance_extend_product_info_request import ShowEngineInstanceExtendProductInfoRequest
from huaweicloudsdkrabbitmq.v2.model.show_engine_instance_extend_product_info_response import ShowEngineInstanceExtendProductInfoResponse
from huaweicloudsdkrabbitmq.v2.model.show_instance_extend_product_info_request import ShowInstanceExtendProductInfoRequest
from huaweicloudsdkrabbitmq.v2.model.show_instance_extend_product_info_resp_hourly import ShowInstanceExtendProductInfoRespHourly
from huaweicloudsdkrabbitmq.v2.model.show_instance_extend_product_info_resp_monthly import ShowInstanceExtendProductInfoRespMonthly
from huaweicloudsdkrabbitmq.v2.model.show_instance_extend_product_info_response import ShowInstanceExtendProductInfoResponse
from huaweicloudsdkrabbitmq.v2.model.show_instance_request import ShowInstanceRequest
from huaweicloudsdkrabbitmq.v2.model.show_instance_resp import ShowInstanceResp
from huaweicloudsdkrabbitmq.v2.model.show_instance_response import ShowInstanceResponse
from huaweicloudsdkrabbitmq.v2.model.show_maintain_windows_request import ShowMaintainWindowsRequest
from huaweicloudsdkrabbitmq.v2.model.show_maintain_windows_response import ShowMaintainWindowsResponse
from huaweicloudsdkrabbitmq.v2.model.show_queue_details_request import ShowQueueDetailsRequest
from huaweicloudsdkrabbitmq.v2.model.show_queue_details_response import ShowQueueDetailsResponse
from huaweicloudsdkrabbitmq.v2.model.show_rabbit_mq_project_tags_request import ShowRabbitMqProjectTagsRequest
from huaweicloudsdkrabbitmq.v2.model.show_rabbit_mq_project_tags_response import ShowRabbitMqProjectTagsResponse
from huaweicloudsdkrabbitmq.v2.model.show_rabbit_mq_tags_request import ShowRabbitMqTagsRequest
from huaweicloudsdkrabbitmq.v2.model.show_rabbit_mq_tags_response import ShowRabbitMqTagsResponse
from huaweicloudsdkrabbitmq.v2.model.show_vhost_detail_resp import ShowVhostDetailResp
from huaweicloudsdkrabbitmq.v2.model.tag_entity import TagEntity
from huaweicloudsdkrabbitmq.v2.model.tag_multy_value_entity import TagMultyValueEntity
from huaweicloudsdkrabbitmq.v2.model.update_instance_req import UpdateInstanceReq
from huaweicloudsdkrabbitmq.v2.model.update_instance_request import UpdateInstanceRequest
from huaweicloudsdkrabbitmq.v2.model.update_instance_response import UpdateInstanceResponse
from huaweicloudsdkrabbitmq.v2.model.update_plugins_req import UpdatePluginsReq
from huaweicloudsdkrabbitmq.v2.model.update_plugins_request import UpdatePluginsRequest
from huaweicloudsdkrabbitmq.v2.model.update_plugins_response import UpdatePluginsResponse
from huaweicloudsdkrabbitmq.v2.model.update_user_request import UpdateUserRequest
from huaweicloudsdkrabbitmq.v2.model.update_user_response import UpdateUserResponse

