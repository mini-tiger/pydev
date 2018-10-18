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
	"host_info": {"0":{}
				  },
	"bk_supplier_id": 0,
	"bk_biz_id": 3
}
