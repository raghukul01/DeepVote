from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .models import Choice, Question
import datetime
import pickle
import subprocess
import requests
# solc is needed to compile our Solidity code
from solc import compile_source

# web3 is needed to interact with eth contracts
from web3 import Web3, HTTPProvider

# we'll use ConciseContract to interact with our specific instance of the contract
from web3.contract import ConciseContract

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    bashCommand = "cp unique_sig_empty unique_sig"+str(question_id)
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    print (question_id)
    question = get_object_or_404(Question, pk=question_id)
    _commit_end = question.pub_date
    # print (type(date))
    # print(int(_commit_end))

    commit_end = int((_commit_end.replace(tzinfo=None) - datetime.datetime(1970,1,1).replace(tzinfo=None)).total_seconds())
    
    # print(commit_end)
    # start of contract work
    
    r=requests.get("http://127.0.0.1:8000/polls/"+str(question_id))
    print(r.content)
    resp=str(r.content).split('\\n')
    print("before strip")
    print(resp)
    resp=[x.strip() for x in resp]

    print("before after")
    print(resp)
    choices=[]
    for i in resp:
        if('label' in i):
            temp=""
            fl=0
            for j in range(1,len(i)):
                if(i[j]=='>'):
                    fl=1
                    continue
                if(i[j]=='<'):
                    fl=0
                if(fl==1):
                    temp+=i[j]
            choices.append(temp)


    http_provider = HTTPProvider('http://localhost:8545')
    eth_provider = Web3(http_provider).eth

    default_account = eth_provider.accounts[0]
    transaction_details = {
        'from': default_account,
    }

    # load our Solidity code into an object
    with open('polls/poll.sol') as file:
        source_code = file.readlines()

    # compile the contract
    compiled_code = compile_source(''.join(source_code))

    # store contract_name so we keep our code DRY
    contract_name = 'pollBooth'

    contract_bytecode = compiled_code[f'<stdin>:{contract_name}']['bin']
    contract_abi = compiled_code[f'<stdin>:{contract_name}']['abi']

    contract_factory = eth_provider.contract(
        abi=contract_abi,
        bytecode=contract_bytecode,
    )

    facultylist = pickle.load(open('conf/faculty.pub', 'rb'))
    
    contract_constructor = contract_factory.constructor(len(choices), len(facultylist),40,70)

    transaction_hash = contract_constructor.transact(transaction_details)

    transaction_receipt = eth_provider.getTransactionReceipt(transaction_hash)
    contract_address = transaction_receipt['contractAddress']

    contract_instance = eth_provider.contract(
        abi=contract_abi,
        address=contract_address,
        ContractFactoryClass=ConciseContract,
    )

    with open ("conf/"+ str(question_id) + "contract_abi", 'wb') as handle:
        pickle.dump(contract_abi, handle, protocol=3)

    with open ("conf/"+ str(question_id) + "contract_address", 'wb') as handle:
        pickle.dump(contract_address, handle, protocol=3)

    with open ("conf/"+ str(question_id) + "ConciseContract", 'wb') as handle:
        pickle.dump(ConciseContract, handle, protocol=3)

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "Contract created.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
