## 怎么样包装你的程序给算子使用
1. 不论是什么语言写的算子，我们统一使用python做封装，写wrapper。
算法的实现可以是能够被python调用的任何语言。算法包需要能在ubuntu 16.04以上版本的环境下能编译运行。
1. 将你的算法或模型封装一个或几个可以供python调用的函数
2. 写一个以你<算子名字>命名的python文件： <算子名字>.py
3. 在<算子名字>.py里，写一个main运行的方式

  * 例子1

```python
# 例子 1

#!/usr/bin/env python
# encoding: utf-8
# import <算子调用函数所在文件>

if __name__ == "__main__":
    #统一使用python包: argparse, 可以把你的程序封装成linux命令行那样方便使用
    import argparse
    parser = argparse.ArgumentParser(description="") 

    # 如果有input文件输入，或者多个文件路径输入(一般指图片目录、时间序列片段目录),
    # 最多只能定义一个positional argument.
    # 一般将主输入（建议选取文本或字符串较长的输入变量）作为input.
    # 注意positional argument是只按位置识别的程序运行参数，默认如果不给的话是从标准输入流传递数据。
    # 这样做保证了类似这样的运行方式  cat <input> | <算子程序> -o output.txt 
    #     举例： cat <input>  | wc -l
    parser.add_argument('input', nargs='?', default=sys.stdin)

	# 对于其他需要的输入文件，则添加其他 option argument，不可作为positional argument
	# parser.add_argument('-m', '--model', nargs='?', default='[filename]') #机器学习模型文件

    # 如果有输出文件则需要给出 “-o” arguments; 如果是多个输出文件，则“-o1  output1  -o2 output2 ....”
    # 如果 ’-o‘ 之后没有参数，那么默认输出到标准输出流
    parser.add_argument("-o", "--output", type=str, default=sys.stdout,
                        help="123")

    # 如果需要其他参数，则自行设计参数的flag，如“-c”
    parser.add_argument("-c", "--colum", nargs='+', type=str,
                        help="")
    parser.add_argument("-d", "--delimeter", type=str, default=',',
                        help="")
    # 版本号
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')

    sargs = parser.parse_args()

    # 利用传入的参数，调用算子函数

```

  * 例子2

```python
    # 例子2
    import argparse
    parser = argparse.ArgumentParser()
    # 主输入
	parser.add_argument('input', nargs='?', default=sys.stdin, help='''\
            The input file name with path.
            eg. ./*.edgelist.
            ''' )
	# 时间序列输入
	parser.add_argument('--propts', nargs=1, type=str, help='''*ts.dict for time series,
            e.g. yelpts.dict[.gz]'''
			)
	# 打分属性输入
	parser.add_argument('--proprt', nargs=1, type=str, help='''*rate.dict for rating,
            e.g. yelprate.dict[.gz]'''
			)
    parser.add_argument('-n', '--nblocks', nargs='?', help='''The number of dense blocks to
            detect (default:1)''', default=1, type=int)
	
	# 枚举可选择的变量值 choices
    parser.add_argument('-m', '--method', nargs='?', help='''The method used to detect fraud''',
            choices=['HS', 'FR'], type=str, default='HS')
    
	# 输出文件路径
	parser.add_argument('-o', '--outpath',
            help="choose number of blocks to detect (default:./testout/).",
            default='./output/')
    
	# bool类型参数
    parser.add_argument('-t', action='store_true',
            help='consider time series. Need *ts.dict[.gz] file')
    parser.add_argument('-s', action='store_true',
            help='consider rating scores. Need *rate.dict[.gz] file')
    args = parser.parse_args()
    
	# 利用传入的参数，调用算子函数
```

4. 写算子描述文件，在json文件中的requirements.txt里写明安装依赖环境的脚本或python包
```json
{
	"conf": {
		// 配置文件版本、类型
		"version": "1.0",
		"type": "operator",
		// 算子配置文件
		"operator": {
			"name": "csvadaptor",
			"cmd": "csvadaptor.py",
			"type": "python",
			"version": "1.0",
			// 算子描述
			"description": "按照需要提取文件中特定的列",
			// 输入文件参数及格式描述
			"input": [
				{
					"name": "input1",
					"format": "csv",
					"description": "输入文件路径",
					// 输入文件格式描述
					"table": [
						{
							"name": "ID",
							"type": "int",
							"min": "1",
							"max": "1.5474250491067253e+26 "
						},
						{
							"name": "Name",
							"type": "string"
						},
						{
							"name": "CountryCode",
							"type": "string"
						},
						{
							"name": "District",
							"type": "string",
							"max": "255"
						}
					]
				}
			],
			// 其他参数描述
			"argument": [
				{
					"name": "colum",
					"type": "tuple",
					"required": "true",
					"description": "需要提取的列，并对应到新文件中"
				},
				{
					"name": "delimeter",
					"type": "string",
					"required": "false",
					"default": ",",
					"description": "输入文件分割符"
				}
			],
			// 输出文件参数及格式
			"output": {
				"name": "output1",
				"format": "csv",
				"description": "输出文件路径，默认为sys.stdout"
				// 如果需要给出输出文件格式
				"table":[
					{

					}
				]
			},
			// 算子运行的依赖需求文件 python 包
			"requirements": {
				"type": "string",
				"default": "/requirements.txt"
			}
		}
	}
}

```

5. 如何封装日志输出 （建议）
  * 简单做法
```python
# 单独封装log的打印，这样后续如果需要输出日志文件也可以方便调整
def log(context):
    print "["+time.ctime()+"]"+context
    sys.stdout.flush()

```
  * 丰富做法利用python包 [logging](https://docs.python.org/3/howto/logging.html#logging-advanced-tutorial)

```python
import logging

# create logger
logger = logging.getLogger('simple_example')
logger.setLevel(logging.DEBUG)
# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)
# 'application' code
logger.debug('debug message')
logger.info('info message')
logger.warning('warn message')
logger.error('error message')
logger.critical('critical message')
```

  * 使用配置文件

```python
import logging
import logging.config

logging.config.fileConfig('logging.conf')

# create logger
logger = logging.getLogger('simpleExample')

# 'application' code
logger.debug('debug message')
logger.info('info message')
logger.warning('warn message')
logger.error('error message')
logger.critical('critical message')

```
logging.conf
```
[loggers]
keys=root,simpleExample

[handlers]
keys=consoleHandler

[formatters]
keys=simpleFormatter

[logger_root]
level=DEBUG
handlers=consoleHandler

[logger_simpleExample]
level=DEBUG
handlers=consoleHandler
qualname=simpleExample
propagate=0

[handler_consoleHandler]
class=StreamHandler
level=DEBUG
formatter=simpleFormatter
args=(sys.stdout,)

[formatter_simpleFormatter]
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
datefmt=
```
输出样式：
```shell
$ python simple_logging_config.py
2005-03-19 15:38:55,977 - simpleExample - DEBUG - debug message
2005-03-19 15:38:55,979 - simpleExample - INFO - info message
2005-03-19 15:38:56,054 - simpleExample - WARNING - warn message
2005-03-19 15:38:56,055 - simpleExample - ERROR - error message
2005-03-19 15:38:56,130 - simpleExample - CRITICAL - critical message
```
