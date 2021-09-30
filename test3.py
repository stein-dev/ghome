import json

jsondata = """
{
  "meta": { "date": "2021-09-28T20:29:17.076Z" },
  "results": [
    {
      "id": "6",
      "name": " ",
      "code": "9DAY_EVERYDAY",
      "banner_link": "https://globeathomeapp.globe.com.ph/cms/s3/cms-v2-voucher-categories/prod/6/banner.png",
      "seq_num": "5",
      "sponsors": [
        {
          "name": "Giftaway",
          "category": "6",
          "cms_vouchers": [
            {
              "category_id": "6",
              "sponsor_name": "Giftaway",
              "id": "217",
              "voucher_sponsors_code": "TENURED_REWARDS_HPW50",
              "category": "917_TENURED_REWARDS",
              "name": "Giftaway",
              "short_description": "P50 Giftaway voucher for Lazada, Shopee, GrabFood, Krispy Kreme, or Jollibee",
              "long_description": " ",
              "spiels": "",
              "target": "specific",
              "type": "linkout",
              "code": "",
              "start_date": "2021-09-16T16:00:00.000Z",
              "end_date": "2021-09-30T15:59:59.000Z",
              "expiration_date": "2021-09-30T15:59:59.000Z",
              "icon": "prod/217/icon.jpg",
              "background_image": "",
              "banner_image": "prod/217/bannerImage.jpg",
              "remarks": "",
              "is_active": "1",
              "is_deleted": "0",
              "addon": "",
              "created_at": "2021-09-09T02:14:42.000Z",
              "updated_at": "2021-09-16T11:47:23.000Z",
              "base_url": "https://globeathomeapp.globe.com.ph/cms/s3/cms-v2-vouchers/",
              "vouchers": [
                {
                  "claimed_at": "",
                  "cms_vouchers_id": "217",
                  "code": "tZcQSRKYOsrMr851LgsIA+aZNyowW2x9svH3mrHz8ptbMRDx1fYq8EimP5SDfCEL",
                  "customer_identifier": "09450425693",
                  "expiration_date": "2021-09-30T15:59:59.000Z",
                  "promo_vouchers_id": "",
                  "subscription_date": "",
                  "subscription_service_id": "",
                  "used_at": "",
                  "voucher_sponsors_code": "TENURED_REWARDS_HPW50"
                }
              ]
            }
          ]
        }
      ]
    },
    {
      "id": "2",
      "name": "LEARN",
      "code": "LEARN",
      "banner_link": "https://globeathomeapp.globe.com.ph/cms/s3/cms-v2-voucher-categories/prod/2/banner.png",
      "seq_num": 3,
      "sponsors": [
        {
          "name": "Skillshare",
          "category": "2",
          "cms_vouchers": [
            {
              "category_id": "2",
              "sponsor_name": "Skillshare",
              "id": "210",
              "voucher_sponsors_code": "PROJECT_VIRGO_SKILLSHARE_HPW",
              "category": "PROJECT_VIRGO_HPW",
              "name": "Skillshare",
              "short_description": "Here's your free 1-month subscription voucher for Skillshare!",
              "long_description": " ",
              "spiels": "",
              "target": "specific",
              "type": "linkout",
              "code": "",
              "start_date": "2021-08-29T00:00:00.000Z",
              "end_date": "2021-11-22T15:59:59.000Z",
              "expiration_date": "2021-11-22T15:59:59.000Z",
              "icon": "prod/210/icon.png",
              "background_image": "",
              "banner_image": "prod/210/bannerImage.png",
              "remarks": "",
              "is_active": "1",
              "is_deleted": "0",
              "addon": "",
              "created_at": "2021-08-27T13:26:38.000Z",
              "updated_at": "2021-08-27T14:57:36.000Z",
              "base_url": "https://globeathomeapp.globe.com.ph/cms/s3/cms-v2-vouchers/",
              "vouchers": [
                {
                  "claimed_at": "",
                  "cms_vouchers_id": "210",
                  "code": "mNfaUVMh4p/3TAY/LydP/N1U+AUG+J2TpQIms/SjK3U=",
                  "customer_identifier": "09450425693",
                  "expiration_date": "2021-11-22T15:59:59.000Z",
                  "promo_vouchers_id": "",
                  "subscription_date": "",
                  "subscription_service_id": "",
                  "used_at": "",
                  "voucher_sponsors_code": "PROJECT_VIRGO_SKILLSHARE_HPW"
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}"""

tmp = json.loads(jsondata)
for tmp in tmp['results']:
  sponsor_name = tmp['sponsors'][0]['cms_vouchers'][0]['sponsor_name']
  desc = tmp['sponsors'][0]['cms_vouchers'][0]['short_description']
  code = tmp['sponsors'][0]['cms_vouchers'][0]['vouchers'][0]['code']
  exp = tmp['sponsors'][0]['cms_vouchers'][0]['vouchers'][0]['expiration_date']
  print(sponsor_name)
  print(desc)
  print(code)
  print(exp)