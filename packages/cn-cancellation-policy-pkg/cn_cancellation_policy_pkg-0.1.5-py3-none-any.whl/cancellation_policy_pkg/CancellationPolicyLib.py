from datetime import datetime, timedelta
import pytz
from typing import List, Dict, Any, Optional


class CancellationPolicy:
    def __init__(self, check_in_date: str):
        self.current_datetime = datetime.now()
        self.free_cancellation_policy = None
        self.check_in_date = check_in_date + "T23:00:00"
        self.partner_cp = []
        self.cn_polices = []

    def format_date(self, date_str: str) -> str:
        if date_str is None:
            return self.current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        # List of possible input date formats
        input_formats = [
            "%Y-%m-%d %H:%M:%S",
            "%Y/%m/%d %H:%M:%S",
            "%d-%m-%Y %H:%M:%S",
            "%d/%m/%Y %H:%M:%S",
            "%m-%d-%Y %H:%M:%S",
            "%m/%d/%Y %H:%M:%S",
            "%m/%d/%Y %H:%M",
            "%Y-%m-%dT%H:%M:%SZ",
            "%m/%d/%Y",
            "%Y-%m-%d",
            "%d-%m-%Y",
            "%y-%m-%d",
            "%d-%m-%y",
            "%Y-%m-%dT%H:%M:%S"
        ]
        for fmt in input_formats:
            try:
                # Parse date_str into datetime object
                dt = datetime.strptime(date_str, fmt)
                # Format datetime object into desired format
                return dt.strftime("%Y-%m-%d %H:%M:%S")
            except ValueError:
                continue
        # If no formats match, return the original string or raise an error
        raise ValueError(f"Date format for {date_str} not recognized")

    def get_check_in_date(self) -> str:
        return self.check_in_date

    def dida_date_format(self, date_str: str) -> str:
        try:
            return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
        except:
            return datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m-%d %H:%M:%S")

    def hp_format_date(self, date_str: str) -> datetime:
        try:
            return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            pass
        try:
            return datetime.strptime(date_str, "%m/%d/%Y")
        except ValueError:
            pass
        try:
            return datetime.strptime(date_str, "%m/%d/%Y %H:%M")
        except ValueError:
            pass
        try:
            return datetime.strptime(date_str, "%d/%m/%Y")
        except ValueError:
            raise ValueError(f"Date format for '{date_str}' is not recognized.")

    def check_deadline_format(self, deadline):
        formats = ["%m/%d/%Y %H:%M", "%m/%d/%Y", "%m/%d/%Y %H:%M:%S", "%m/%d/%Y %H:%M:%S:%A", "%Y-%m-%dT%H:%M:%SZ"]
        for fmt in formats:
            try:
                datetime.strptime(deadline, fmt)
                return fmt
            except ValueError:
                continue
        return "Unknown format"

    def round_time(self, time_str):
        # Parse the time string into a datetime object
        dt = datetime.strptime(time_str, '%I:%M %p')

        # Round the time to the nearest half-hour
        rounded_minute = (dt.minute // 30) * 30
        rounded_dt = dt.replace(minute=rounded_minute, second=0, microsecond=0)

        # If rounding up would exceed current time, round down instead
        if rounded_dt > dt:
            rounded_dt -= timedelta(minutes=30)
        return rounded_dt.strftime('%I:%M %p')

    def tbo_format_date(self, date_str: str) -> datetime:
        return datetime.strptime(date_str, "%d-%m-%Y %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")

    def parse_cancellation_policies(self, total_partner: float) -> Dict[str, Any]:
        try:
            cancellation_policies_text = []
            parsed_policies = self.partner_cp
            free_cancellation = self.free_cancellation_policy
            if self.free_cancellation_policy:
                cancellation_type = "Free cancellation"
            else:
                cancellation_type = "Non-Refundable"

            partial_booking = False
            cp_dates_added = []
            cp_i = 0
            end_policy = False
            first_free_sts = False
            if parsed_policies and len(parsed_policies) > 0:
                for key, policy in enumerate(parsed_policies):
                    ref_amt = 100 - ((total_partner - float(policy['amount'])) / total_partner) * 100
                    ref_amt = round(ref_amt)

                    if ref_amt == 0:
                        if first_free_sts:
                            cancellation_policies_text.pop()
                        ref_amt = 100
                        free_cancellation = True
                        first_free_sts = True
                        cancellation_type = "Free cancellation"
                    elif ref_amt == 100:
                        if cp_i == 0 and self.current_datetime.strftime("%Y-%m-%d %H:%M:%S") < policy['start']:
                            ref_amt = 100
                            free_cancellation = True
                            first_free_sts = True
                            cancellation_policies_text
                            cancellation_type = "Free cancellation"
                            policy['end'] = policy['start']
                        else:
                            ref_amt = 0
                            end_policy = True

                        # ref_amt = 0
                        # end_policy = True

                    if ref_amt > 0:
                        partial_booking = True

                    replace_start = str(policy['start'])
                    time_start = datetime.strptime(replace_start, '%Y-%m-%d %H:%M:%S').strftime('%I:%M %p')
                    time_start = self.round_time(time_start)
                    date_start = datetime.strptime(replace_start, '%Y-%m-%d %H:%M:%S').strftime('%d %b %Y')

                    replace_end = str(policy['end'])
                    time_end = datetime.strptime(replace_end, '%Y-%m-%d %H:%M:%S').strftime('%I:%M %p')
                    time_end = self.round_time(time_end)
                    date_end = datetime.strptime(replace_end, '%Y-%m-%d %H:%M:%S').strftime('%d %b %Y')

                    start_date_str = date_start + ' ' + time_start
                    end_date_str = date_end + ' ' + time_end

                    if free_cancellation and cp_i == 0:
                        cancellation_policies_text.append(
                            f"Receive a {ref_amt}% refund for your booking if you cancel before {date_end} at {time_end}")
                    elif cp_i == 0:
                        cancellation_policies_text.append(
                            f"Receive a {ref_amt}% refund for your booking if you cancel before {date_end} at {time_end}")
                    else:
                        if ref_amt != 0:
                            cancellation_policies_text.append(
                                f"Receive a {ref_amt}% refund for your booking if you cancel between {start_date_str} and {end_date_str}")
                    cp_i += 1

                if end_policy:
                    cancellation_policies_text.append(
                        f"If you cancel your reservation after {start_date_str}, you will not receive a refund. The booking will be non-refundable.")
                else:
                    cancellation_policies_text.append(
                        f"If you cancel your reservation after {end_date_str}, you will not receive a refund. The booking will be non-refundable.")

                if not partial_booking and not free_cancellation:
                    cancellation_type = "Non-Refundable"
                    cancellation_policies_text = ["You won't be refunded if you cancel this booking"]
                elif not free_cancellation and partial_booking:
                    cancellation_type = "Partial refund"
            else:
                cancellation_type = "Non-Refundable"
                cancellation_policies_text = ["You won't be refunded if you cancel this booking"]

            self.cn_polices = {
                'type': cancellation_type,
                'text': cancellation_policies_text
            }
            return self.cn_polices
        except Exception as ex:
            print(f"Exception : {str(ex)}")
            self.cn_polices = {
                'type': '',
                'text': ''
            }
            return self.cn_polices

    # parse ratehawk cancellation policy
    def parse_ratehawk_cancellation_policy(self, pricing: List[Dict[str, Any]], total_price: float) -> List[
        Dict[str, Any]]:
        try:
            cp = []
            if 'cancellation_penalties' in pricing[0] and 'policies' in pricing[0]['cancellation_penalties']:
                check_in_date = self.get_check_in_date()
                i = 0
                last_date = None
                for policy in pricing[0]['cancellation_penalties']['policies']:
                    start_at = policy.get('start_at', datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))
                    end_at = policy.get('end_at', check_in_date)
                    if start_at is None and end_at is None:
                        continue
                    if i == 0:
                        if start_at is None:
                            start_at = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
                    else:
                        start_at = last_date
                    if (end_at is None):
                        end_at = check_in_date
                    last_date = end_at
                    i += 1
                    p_amount = int(round(float(policy['amount_show']), 0))
                    if p_amount == 0:
                        amount_rtn = 0
                    elif p_amount == total_price:
                        amount_rtn = total_price
                    else:
                        amount_rtn = total_price - p_amount
                    self.partner_cp.append({
                        'start': self.format_date(start_at),
                        'end': self.format_date(end_at),
                        'amount': amount_rtn,
                        'currency': pricing[0]['currency_code'] if 'currency_code' in pricing[0] else "USD"
                    })
                    free_cancellation_before = pricing[0]["cancellation_penalties"]["free_cancellation_before"]
                    if free_cancellation_before is None or free_cancellation_before == "":
                        free_cancellation_before = None
                    if policy[
                        'amount_show'] == '0.00' and free_cancellation_before is not None and self.free_cancellation_policy is None:
                        self.free_cancellation_policy = True
            cancellation_policy = self.parse_cancellation_policies(total_price)
            return cancellation_policy
        except Exception as ex:
            print(f"Exception : {str(ex)}")
            cancellation_policy = self.parse_cancellation_policies(total_price)
            return cancellation_policy

            # Rakuten provide in UTC timezone

    def parse_rakuten_cancellation_policy(self, room_data: Dict[str, Any], total_price: float) -> List[Dict[str, Any]]:
        try:
            cancellation_policies = []
            policy_rules = room_data['cancellation_policy']
            currency_code = room_data['room_rate_currency']
            policies = policy_rules['cancellation_policies']
            for rule_data in policies:

                if 'date_from' in rule_data and rule_data['date_from']:
                    start_date = self.format_date(rule_data['date_from'])
                    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
                    if start_date_obj < self.current_datetime:
                        start_date = self.current_datetime.strftime("%Y-%m-%d %H:%M:%S")


                else:
                    start_date = self.current_datetime.strftime("%Y-%m-%d %H:%M:%S")
                    start_date_obj = self.current_datetime

                if 'date_to' in rule_data and rule_data['date_to']:
                    end_date = self.format_date(rule_data['date_to'])
                    end_date_obj = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")
                else:
                    end_date = self.current_datetime.strftime("%Y-%m-%d %H:%M:%S")
                    end_date_obj = self.current_datetime
                # case 1 as per rakuten cancellation_policy will regularly return a date that is already in the past (i.e. 1999-01-01T17:47:00Z) This indicates that the penalty_percentage applies from the time of booking
                if start_date_obj < self.current_datetime and end_date_obj < self.current_datetime:
                    continue
                if start_date_obj > self.current_datetime and end_date_obj <= self.current_datetime:
                    end_date = self.format_date(self.get_check_in_date())

                room_price = total_price
                if rule_data['penalty_percentage'] == 0:
                    percentage = 0
                elif rule_data['penalty_percentage'] == 100:
                    percentage = 100
                else:
                    percentage = 100 - rule_data['penalty_percentage']
                amount_percentage = room_price / 100
                percentage_amount = int(round(amount_percentage * percentage))
                cp = {
                    'start': start_date,
                    'end': end_date,
                    'amount': percentage_amount,
                    'currency': currency_code
                }
                cancellation_policies.append(cp)
                if rule_data['penalty_percentage'] == 0 and self.free_cancellation_policy is None:
                    self.free_cancellation_policy = True
            self.partner_cp = cancellation_policies
            print(f"RK Partner CP : {self.partner_cp}")
            cancellation_policy = self.parse_cancellation_policies(total_price)
            return cancellation_policy
        except Exception as ex:
            print(f"Exception : {str(ex)}")
            cancellation_policy = self.parse_cancellation_policies(total_price)
            return cancellation_policy

    # please be kindly note all the cancelation are based on Beijing time
    def parse_dida_cancellation_policy(self, pricing: Dict[str, Any], total_price: float) -> List[Dict[str, Any]]:
        try:
            cp = []
            check_in_date = self.format_date(self.get_check_in_date())
            if 'RatePlanCancellationPolicyList' in pricing and len(pricing['RatePlanCancellationPolicyList']) > 0:
                temp_array = []
                i = 0
                last_date = None

                for k, policy in enumerate(pricing['RatePlanCancellationPolicyList']):
                    if i == 0:
                        start_at = self.current_datetime.strftime("%Y-%m-%d %H:%M:%S")
                    else:
                        start_at = last_date
                    end_at = policy.get('FromDate', check_in_date)
                    end_at = self.dida_date_format(end_at)
                    end_date_obj = datetime.strptime(end_at, "%Y-%m-%d %H:%M:%S")
                    if end_date_obj < self.current_datetime:
                        continue
                        # end_at = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
                    last_date = end_at
                    i += 1
                    p_amount = int(round(policy['Amount'], 0))
                    if p_amount == 0:
                        amount_rtn = 0
                    elif p_amount == total_price:
                        amount_rtn = total_price
                    else:
                        amount_rtn = total_price - p_amount
                    self.partner_cp.append({
                        'start': start_at,  # date format (2021-07-11 00:00:00)
                        'end': end_at,
                        'amount': amount_rtn,
                        'currency': pricing['Currency']
                    })
                    if policy['Amount'] == 0 and self.free_cancellation_policy is None:
                        self.free_cancellation_policy = True
            cancellation_policy = self.parse_cancellation_policies(total_price)
            return cancellation_policy
        except Exception as ex:
            print(f"Exception : {str(ex)}")
            cancellation_policy = self.parse_cancellation_policies(total_price)
            return cancellation_policy

    # Hp provide in UTC timezone
    def parse_hp_cancellation_policy(self, pricing: Dict[str, Any], total_hp: float, pernight_amount: float) -> List[
        Dict[str, Any]]:
        try:
            global free_cancellation_policy
            cancellation_policies = []
            temp_array = []
            current_datetime = datetime.now()
            s_end_date = None
            nonRefundable = pricing.get('nonRefundable', None)
            if nonRefundable is None or nonRefundable is True:
                cancellation_policy = self.parse_cancellation_policies(total_hp)
                return cancellation_policy
            if 'freeCancellationCutOff' in pricing and pricing['freeCancellationCutOff']:
                s_start_at = current_datetime
                s_end_date = self.format_date(pricing['freeCancellationCutOff'])
                s_start_at = s_start_at.strftime("%Y-%m-%d %H:%M:%S")
                # s_end_date = s_end_date.strftime("%Y-%m-%d %H:%M:%S")
                if s_end_date > s_start_at:
                    first_cp = {
                        'start': s_start_at,
                        'end': s_end_date,
                        'amount': 0,
                        'currency': pricing.get('currencyCode', 'USD')
                    }
                    self.partner_cp.append(first_cp)
                    cancellation_policies.append(first_cp)
            last_date = None
            # deadlines = [penalty['deadline'] for penalty in pricing['cancelPenalties']]
            # formats = [check_deadline_format(deadline) for deadline in deadlines]
            # pricing['cancelPenalties'] = sorted(pricing['cancelPenalties'], key=lambda x: datetime.strptime(x['deadline'], formats))
            cancel_penalties = pricing.get('cancelPenalties', [])
            if not cancel_penalties:
                pass
            else:
                for penalty in pricing['cancelPenalties']:
                    penalty['format'] = self.check_deadline_format(penalty['deadline'])
                # Sort the cancelPenalties using the determined formats
                pricing['cancelPenalties'] = sorted(
                    pricing['cancelPenalties'],
                    key=lambda x: datetime.strptime(x['deadline'], x['format'])
                )
                for i, policy in enumerate(pricing['cancelPenalties']):
                    if policy not in temp_array and 'deadline' in policy and policy['deadline']:
                        temp_array.append(policy)
                        if i == 0 and s_end_date is not None:
                            start_at = s_end_date
                        elif i == 0:
                            start_at = current_datetime
                        else:
                            start_at = last_date
                        end_at_str = policy['deadline'].replace(',', '')

                        end_at = self.hp_format_date(end_at_str)
                        if end_at == start_at:
                            continue
                        if end_at < current_datetime:
                            continue
                        last_date = end_at
                        i += 1
                        price_type = policy.get('type', '')
                        if price_type == 'price':
                            amount = policy.get('price', policy.get('amount', 0))
                        else:
                            no_of_night = policy.get('nights', 1)
                            amount = no_of_night * pernight_amount
                        if isinstance(start_at, str):
                            s_check_date = datetime.strptime(start_at, "%Y-%m-%d %H:%M:%S")
                        else:
                            s_check_date = datetime.strptime(start_at.strftime("%Y-%m-%d %H:%M:%S"),
                                                             "%Y-%m-%d %H:%M:%S")
                        if isinstance(end_at, str):
                            e_check_date = datetime.strptime(end_at, "%Y-%m-%d %H:%M:%S")
                        else:
                            e_check_date = datetime.strptime(end_at.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
                        if e_check_date < s_check_date:
                            continue
                        if amount == 0:
                            ret_amount = 0
                        else:
                            ret_amount = total_hp - amount if total_hp > amount else total_hp
                        if isinstance(start_at, str):
                            date_strt = self.format_date(start_at)
                        else:
                            date_strt = start_at.strftime("%Y-%m-%d %H:%M:%S")
                        if isinstance(end_at, str):
                            date_end = self.format_date(end_at)
                        else:
                            date_end = end_at.strftime("%Y-%m-%d %H:%M:%S")
                        cp = {
                            'start': date_strt,
                            'end': date_end,
                            'amount': ret_amount,
                            'currency': pricing.get('currencyCode', 'USD')
                        }
                        cancellation_policies.append(cp)
                if pricing.get('freeCancellation') and self.free_cancellation_policy is None:
                    self.free_cancellation_policy = True
                self.partner_cp = cancellation_policies
            cancellation_policy_data = self.parse_cancellation_policies(total_hp)
            return cancellation_policy_data
        except Exception as ex:
            print(f"Exception : {str(ex)}")
            cancellation_policy = self.parse_cancellation_policies(total_hp)
            return cancellation_policy

    # Tbo cancellation policy method
    # please be kindly note all the cancelation are based on Beijing time
    def parse_tbo_cancellation_policy(self, pricing: Dict[str, Any], total_tbo: float) -> List[Dict[str, Any]]:
        try:
            global free_cancellation_policy
            cp = []
            total_tbo = int(round(total_tbo))
            check_in_date = self.format_date(self.get_check_in_date())
            # Sort the cancelPenalties using the determined formats
            pricing = sorted(pricing, key=lambda x: datetime.strptime(x['FromDate'], '%d-%m-%Y %H:%M:%S'))
            if len(pricing) > 0:
                temp_array = []
                i = 0
                last_date = None

                for k, policy in enumerate(pricing):
                    if i == 0:
                        start_at = self.current_datetime.strftime("%Y-%m-%d %H:%M:%S")
                    else:
                        start_at = last_date
                    end_at = policy.get('FromDate', check_in_date)
                    end_at = self.tbo_format_date(end_at)
                    end_date_obj = datetime.strptime(end_at, "%Y-%m-%d %H:%M:%S")
                    if end_date_obj < self.current_datetime:
                        continue
                        # end_at = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
                    last_date = end_at
                    i += 1
                    if policy['ChargeType'] == 'Fixed':
                        if int(round(policy['CancellationCharge'])) == total_tbo:
                            can_amount = total_tbo
                            continue
                        elif int(round(policy['CancellationCharge'])) == 0:
                            can_amount = 0
                        else:
                            can_amount = total_tbo - int(round(policy['CancellationCharge']))
                    else:
                        percentage = int(round(policy['CancellationCharge']))
                        percentage = int(round(percentage))
                        percentage = int(round((percentage / 100) * total_tbo))
                        if percentage == total_tbo:
                            can_amount = total_tbo
                            continue
                        elif percentage == 0:
                            can_amount = 0
                        else:
                            can_amount = total_tbo - percentage
                    self.partner_cp.append({
                        'start': start_at,  # date format (2021-07-11 00:00:00)
                        'end': end_at,
                        'amount': can_amount,
                        'currency': 'USD'
                    })
                    if can_amount == 0 and self.free_cancellation_policy is None:
                        self.free_cancellation_policy = True
            cancellation_policy_data = self.parse_cancellation_policies(total_tbo)
            return cancellation_policy_data
        except Exception as ex:
            print(f"Exception : {str(ex)}")
            cancellation_policy = self.parse_cancellation_policies(total_tbo)
            return cancellation_policy

    # this method will convert property cancellation policy according to the property timezone
    def convert_to_timezone(self, date_str, from_tz_str, to_tz_str):
        try:
            from_tz = pytz.timezone(from_tz_str)
            to_tz = pytz.timezone(to_tz_str)

            # Parse the date string
            naive_datetime = datetime.strptime(date_str, '%d %b %Y %I:%M %p')
            # Localize to the from_tz
            localized_datetime = from_tz.localize(naive_datetime)
            # Convert to the target timezone
            converted_datetime = localized_datetime.astimezone(to_tz)
            return converted_datetime
        except Exception as ex:
            print(f"Exception : {str(ex)}")
            return []

