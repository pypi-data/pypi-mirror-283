from osbot_utils.base_classes.Type_Safe import Type_Safe


class LLMs__Platforms(Type_Safe):

    def model_options(self):
        return { 'Groq (Free)'       : { 'Meta'         : { 'LLaMA3 8b'          : 'llama3-8b-8192'                            ,
                                                            'LLaMA3 70b'         : 'llama3-70b-8192'                            },
                                         'Mistral'      : { 'Mixtral 8x7b'       : 'mixtral-8x7b-32768'                        },
                                         'Google'       : { 'Gemma 7b'           : 'gemma-7b-it'                               }},

                 'Open Router (Free)': { 'Google'       : { 'Gemma 7b'           : 'google/gemma-7b-it:free'                   ,
                                                            'Gemma 9b'           : 'google/gemma-2-9b-it:free'                 },
                                         'Meta'         : { 'LLaMA3 8b'          : 'meta-llama/llama-3-8b-instruct:free'       },
                                         'Microsoft'    : { 'Phi-3 Medium 128K'  : 'microsoft/phi-3-medium-128k-instruct:free' ,
                                                            'Phi-3 Mini 128K'    : 'microsoft/phi-3-mini-128k-instruct:free'   },
                                         'Nous Research': { 'Capybara 7b'        : 'nousresearch/nous-capybara-7b:free'        },
                                         'Open Chat'    : { 'Openchat 7b'        : 'openchat/openchat-7b:free'                 },
                                         'Gryphe'       : { 'Mythomist 7b'       : 'gryphe/mythomist-7b:free'                  },
                                         'Wild 7B'      : { 'Toppy M 7b'         : 'undi95/toppy-m-7b:free'                    },
                                         'Hugging Face' : { 'Zephyr 7b'          : 'huggingfaceh4/zephyr-7b-beta:free'         },
                                         'Mistral'      : { 'Mistral 7b Instruct': 'mistralai/mistral-7b-instruct:free'        }},
                'Open Router (Paid)' : { 'Qwen'         : { 'Qwen 2 72B'         : 'qwen/qwen-2-72b-instruct'                  },
                                         'Anthropic'    : { 'Claude 3.5 Sonnet'  : 'anthropic/claude-3.5-sonnet'               },
                                         'Gryphe'       : { 'MythoMax 13b'       : 'gryphe/mythomax-l2-13b'                    },
                                         'Meta'         : { 'Llama3 70b Instruct': 'meta-llama/llama-3-70b-instruct'           },
                                         'Microsoft'    : { 'WizardLM-2 8x22b'   : 'microsoft/wizardlm-2-8x22b'                },
                                         'Nvidia'       : { 'Nemotron-4 340b'    : 'nvidia/nemotron-4-340b-instruct'           },
                                         'Google'       : { 'Gemini Flash 1.5'   : 'google/gemini-flash-1.5'                   ,
                                                            'Gemma 9b'           : 'google/gemma-2-9b-it'                      },
                                         'Sao10K'       : { 'Llama3 Euryale 70b' : 'sao10k/l3-euryale-70b'                     }},

                 'Ollama (Local)'    : { 'Meta'         : { 'LLaMA3 8b'          : 'llama3'                                     },
                                         'Microsoft'    : { 'Phi 3b (Mini)'      : 'phi3'                                       },
                                         'Google'       : { 'Gemma 7b'           : 'gemma'                                     }},

                 'OpenAI (Paid)'     : { 'OpenAI'       : { 'GPT 4o'             : 'gpt-4o'                                    ,
                                                            'GPT 4 Turbo'        : 'gpt-4-turbo'                               ,
                                                            'GPT 3.5 Turbo'      : 'gpt-3.5-turbo'                             }}}


