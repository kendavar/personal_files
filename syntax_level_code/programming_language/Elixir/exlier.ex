#comments in elixir
#This is a comment

#string interpulation
"#{<variable name>} is #{<variable name>}"

#File read and write
def save(deck, filename) do
    binary = :erlang.term_to_binary(deck)
    File.write(filename, binary)
end

def load(filename) do
    {status, binary} = File.read(filename)
    case status do
        :ok -> :erland.binary_to_term binary
        :error -> "That file does not exist"
    end
end
****************************************************************************************************
#working with lists
##shuffle a list##
Enum.shuffle(<list>)

##split a list##
Enum.split(<list>,number) #It generated two list with the number of elements in the number.

## search a element##
Enum.member?(<list>, element)

##install dependency
#go to mix.exe file,
#then in dep module add. This for installing documentation package.
{:ex_doc, "~> 0.12"} <atom and name of the package,<version>
#Then in command line
$mix deps.get

*************************************************************************
#Adding module level documentation
 @moduledoc """
  Provides methods for creating and handling a deck of cards
  """
#Then
$mix docs

#Adding function level documentation
 @doc """
  Returns a list of strings representing a deck of playing cards
  """
#Then
$mix docs


#Adding examples
  @doc """
  Divides a deck into a hand and the remainder of the deck.
  The `hand_size` argument indicates how many cards should
  be in the hand.

  ## Examples
      iex> deck = Cards.create_deck
      iex> {hand, deck} = Cards.deal(deck, 1)
      iex> hand
      ["Ace of Spades"]

  """
  #Here we need to give ## to define a example. Then
  #four spaces to make it look like a code.

