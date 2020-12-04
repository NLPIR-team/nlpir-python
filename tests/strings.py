import os


test_str = "法国启蒙思想家孟德斯鸠曾说过：“一切有权力的人都容易滥用权力，这是一条千古不变的经验。有权力的人直到把权力用到" \
           "极限方可休止。”另一法国启蒙思想家卢梭从社会契约论的观点出发，认为国家权力是公民让渡其全部“自然权利”而获得的，" \
           "他在其名著《社会契约论》中写道：“任何国家权力无不是以民众的权力（权利）让渡与公众认可作为前提的”。"
test_str_1st = "法国启蒙思想家孟德斯鸠曾说过"
test_str_2nd = "另一法国启蒙思想家卢梭从社会契约论的观点出发，认为国家权力是公民让渡其全部“自然权利”而获得的"
test_source_filename = os.path.join(os.path.dirname(__file__), "test.txt")
test_result_filename = os.path.join(os.path.dirname(__file__), "test_result.txt")
user_dict_path = os.path.join(os.path.dirname(__file__), "tmp_user_dict.txt")
