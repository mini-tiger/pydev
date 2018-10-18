# -*- coding: utf-8 -*-
tmpHostSearch = {
	"ip": {
		"data": [],
		"exact": 1,
		"flag": "bk_host_innerip"
	},
	"condition": [
		{
			"bk_obj_id": "host",
			"fields": [],
			"condition": []
		},

	],
	"page": {
		"start": 0,
		"limit": 500,
		"sort": "bk_host_name"
	},
	"pattern": ""
}

# tmpDstBizSearch={
# 	"page": {
# 		"start": 0,
# 		"limit": 10,
# 		"sort": ""
# 	},
# 	"fields": [],
# 	"condition": {}
# }
tmpBizSearch = {
	"bk_supplier_id": 0,
	"fields": [
		# "bk_biz_id",
		# "bk_biz_name"
	],
	"condition": {

	},
	"page": {
		"start": 0,
		"limit": 10,
		"sort": ""
	}
}

tmpAddHost = {
	"host_info": {"0":
					  {"bk_host_innerip": "127.0.0.5",
					   "import_from": "3",
						"bk_cpu":4,
					   'bk_isp_name': '',
					   'bk_province_name': '',
					   	'bk_os_name': 'Windows Server 2012 R2 Standard',
					   'bk_os_version': '6.3.9600 Build 9600',
					   'bk_disk': 299,
					   'operator': '',
					    'bk_mem': 16383,
					   'bk_host_name': 'WIN-G4IPIHKC79C',
					   'bk_comment': '',
					   'bk_os_bit': '',
					   'bk_outer_mac': '',
					   'bk_asset_id': '',
					   'bk_service_term': None,
					   'bk_os_type': '2',
					   'bk_mac': '00:50:56:92:61:ad',
					   'bk_bak_operator': '',
					   'bk_state_name': '',
					   'bk_cpu_module': 'Intel(R) Xeon(R) CPU E7-4820 v3 @ 1.90GHz',
					    'bk_sla': None,
					   'bk_cpu_mhz': 2299,
					   'bk_host_outerip': '',
					   'bk_sn': '',
					   }
				  },
	"bk_supplier_id": 0,
	"bk_biz_id": 3
}
